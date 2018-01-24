"""
The `fill_daily_historical_prices` task can be run manually inside the Django
shell:

```
(venv) $ python manage.py shell
>>> from api.tasks import fill_daily_historical_prices
>>> fill_daily_historical_prices()
```
"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from api.tokens import account_activation_token

import pytz
import time
import requests
from datetime import datetime, date
from api.models import Price, Position, Coin
# from api.allocator import CVaR
from api.allocator import MVO


@shared_task
def allocate_for_user(pk, symbols, risk_score):
    """
    Rebalances portfolio allocations.
    """
    user = get_user_model().objects.get(pk=pk)

    start = datetime(year=2017, month=1, day=1)
    # allocator = CVaR(symbols=symbols, start=start)
    allocator = MVO(symbols=symbols, start=start)
    allocations = allocator.allocate()
    allocation = allocations.loc[risk_score-1]

    user.portfolio.positions.all().delete()

    for symbol in symbols:
        position = Position(
            coin=Coin.objects.get(symbol=symbol),
            amount=allocation[symbol],
            portfolio=user.portfolio
        )
        position.save()
        user.portfolio.positions.add(position)

    user.portfolio.save()
    user.save()


@shared_task
def send_confirmation_email(pk, recipient, site_url):
    user = get_user_model().objects.get(pk=pk)
    email_context = {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'site_url': site_url
    }
    text_content = render_to_string(
        'account_activation_email.txt', email_context
    )
    html_content = render_to_string(
        'account_activation_email.html', email_context
    )
    mail_subject = 'Activate your Polyledger account'
    sender = 'Ari at Polyledger <ari@polyledger.com>'
    email = EmailMultiAlternatives(
        mail_subject,
        text_content,
        sender,
        to=[recipient]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


@shared_task
def fill_daily_historical_prices(coins=Coin.objects.all()):
    """
    Fills the database with historical price data.
    """

    tzinfo = pytz.UTC
    today = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=tzinfo)

    def get_prices(coin, limit=None):
        url = 'https://min-api.cryptocompare.com/data/histoday'
        toTs = time.mktime(today.timetuple())
        params = {
            'tsym': 'USD',
            'toTs': toTs,
            'fsym': coin.symbol
        }
        if limit:
            params['limit'] = limit
        else:
            params['allData'] = True
        response = requests.get(url, params=params)
        prices = response.json()['Data']
        del prices[0]

        for price in prices:
            timestamp = int(price['time'])
            price = price['close']
            instance, created = Price.objects.update_or_create(
                date=date.fromtimestamp(timestamp),
                coin=coin,
                price=price)
            instance.save()
        print('Price update for {0} complete.'.format(coin.name))

    for coin in coins:
        print('Checking prices for {0}'.format(coin.name))
        queryset = Price.objects.filter(coin=coin).order_by('-date')

        if not queryset:
            print('Fetching prices for {0}...'.format(coin.name))
            get_prices(coin)
        else:
            last_date_updated = queryset.first().date

            if today.date() > last_date_updated:
                limit = (today.date() - last_date_updated).days
                print('Fetching prices of {0} for past {1} day(s)'
                      .format(coin.name, limit))
                get_prices(coin, limit=limit)


@shared_task
def get_current_prices(coins=Coin.objects.all()):
    """
    Gets the current price
    """
    today = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=pytz.UTC)
    url = 'https://min-api.cryptocompare.com/data/pricemulti'
    params = {
        'fsyms': ','.join(coins.values_list('name', flat=True)),
        'tsyms': 'USD',
        'allData': 'true'
    }

    response = requests.get(url, params=params)
    data = response.json()

    for coin in data:
        price = coin['USD']
        instance, created = Price.objects.update_or_create(
            date=today,
            coin=coin,
            price=price)
