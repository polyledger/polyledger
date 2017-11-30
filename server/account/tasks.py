from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.schedules import crontab
from django.contrib.auth import get_user_model

import os
from lattice.optimize import Allocator


@shared_task
def allocate_for_user(pk):
    """
    Rebalances portfolio allocations.
    """
    user = get_user_model().objects.get(pk=pk)
    risk_score = user.profile.risk_assessment_score

    coin_map = {
        'bitcoin': 'BTC',
        'litecoin': 'LTC',
        'ethereum': 'ETH',
        'ripple': 'XRP',
        'monero': 'XMR',
        'zcash': 'ZEC',
        'bitcoin_cash': 'BCH',
        'ethereum_classic': 'ETC',
        'neo': 'NEO',
        'dash': 'DASH'
    }

    inv_coin_map = {v: k for k, v in coin_map.items()}

    coins = []
    for coin in sorted(user.portfolio.selected_coins):
        coins.append(coin_map[coin])
    allocator = Allocator(coins=coins, start='2017-10-01')
    allocation = allocator.allocate().loc[risk_score]

    for coin in coin_map.keys():
        setattr(user.portfolio, coin, 0.0)

    for coin in allocation.keys():
        setattr(user.portfolio, inv_coin_map[coin], allocation[coin])
    user.portfolio.save()
    user.save()


@shared_task
def rebalance():
    """
    Rebalances portfolio allocations.
    """
    allocator = Allocator(start='2017-01-01')
    allocations = allocator.allocate()