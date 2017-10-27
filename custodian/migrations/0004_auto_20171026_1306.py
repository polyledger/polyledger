# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custodian', '0003_auto_20171026_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='pair',
            field=models.CharField(choices=[('BTC-USD', 'Bitcoin - US Dollar'), ('ETH-USD', 'Ethereum - US Dollar'), ('LTC-USD', 'Litecoin - US Dollar'), ('ETH-BTC', 'Ethereum - Bitcoin'), ('LTC-BTC', 'Litecoin - Bitcoin')], max_length=9),
        ),
    ]
