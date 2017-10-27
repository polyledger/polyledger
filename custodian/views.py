import os
import gdax
import json
import coinbase
from lattice.optimize import allocate

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from account.models import Portfolio, Profile, Transfer
from custodian.models import Trade

GDAX_API_KEY = os.environ.get('GDAX_API_KEY')
GDAX_SECRET_KEY = os.environ.get('GDAX_SECRET_KEY')
GDAX_PASSPHRASE = os.environ.get('GDAX_PASSPHRASE')
COINBASE_ACCOUNT_ID = os.environ.get('COINBASE_ACCOUNT_ID')


@csrf_exempt
@require_POST
def deposit(request):
    """
    This is an endpoint for Stripe to notify the Account app when a deposit is
    pending, succeeded, or failed. On success, the funds will be deposited into
    the correct exchanges for trading.
    """
    body = json.loads(request.body)
    stripe_charge_id = body['data']['object']['id']
    try:
        profile = Profile.objects.get(
            stripe_customer_id=body['data']['object']['customer']
        )
    except Profile.DoesNotExist:
        print('Profile.DoesNotExist error occurred.')
        # Temporarily handle with a 500. Stripe seems to also return a non-
        # existing customer id in test mode.
        return HttpResponse(status=500)

    user = get_user_model().objects.get(pk=profile.user_id)
    status = body['type'].split('.')[1]
    transfer, created = Transfer.objects.get_or_create(
        user=user,
        transfer_type='deposit',
        amount=body['data']['object']['amount'],
        currency='USD',
        stripe_charge_id=stripe_charge_id,
        exchange='GDAX'
    )
    transfer.status = status
    transfer.save()

    if status == 'succeeded':
        # TODO: Transfer from Stripe to Coinbase

        # Transfer from Coinbase USD wallet to GDAX
        api_url='https://api-public.sandbox.gdax.com'
        auth_client = gdax.AuthenticatedClient(
            GDAX_API_KEY, GDAX_SECRET_KEY, GDAX_PASSPHRASE, api_url=api_url
        )
        deposit_params = {
            'amount': float(transfer.amount), # Does not accept Decimal type
            'coinbase_account_id': COINBASE_ACCOUNT_ID
        }
        auth_client.deposit(deposit_params)

        # Create portfolio
        risk_index = user.profile.risk_assessment_score
        allocation = allocate(risk_index).to_dict()

        # Place trades
        usd = user.portfolio.usd

        for coin in allocation:
            funds = allocation[coin] * usd
            pair = '{0}-USD'.format(coin)
            res = auth_client.buy(funds=funds, product_id=pair, type='market')
            order_id = res.id
            trade = Trade(
                user=user, trade_type='buy', base=coin, quote='USD', pair=pair,
                exchange='GDAX', amount=res.filled_size, cost_basis=funds,
                fees=res.fill_fees, status=res.status, settled=res.settled
            )
            trade.save()
    return HttpResponse(status=204)

def withdraw(request):
    """
    Initiates a withdraw from GDAX.
    """
    pass
