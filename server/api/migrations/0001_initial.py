# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-22 04:19
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('symbol', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('risk_score', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('usd', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Coin')),
                ('portfolio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='api.Portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(unique=True)),
                ('BTC', models.FloatField(null=True)),
                ('ETH', models.FloatField(null=True)),
                ('BCH', models.FloatField(null=True)),
                ('XRP', models.FloatField(null=True)),
                ('LTC', models.FloatField(null=True)),
                ('DASH', models.FloatField(null=True)),
                ('ZEC', models.FloatField(null=True)),
                ('XMR', models.FloatField(null=True)),
                ('ETC', models.FloatField(null=True)),
                ('NEO', models.FloatField(null=True)),
                ('XLM', models.FloatField(null=True)),
                ('ADA', models.FloatField(null=True)),
                ('EOS', models.FloatField(null=True)),
                ('NXT', models.FloatField(null=True)),
                ('QTUM', models.FloatField(null=True)),
                ('OMG', models.FloatField(null=True)),
                ('XEM', models.FloatField(null=True)),
                ('MCO', models.FloatField(null=True)),
                ('KNC', models.FloatField(null=True)),
                ('BTS', models.FloatField(null=True)),
                ('SC', models.FloatField(null=True)),
                ('VTC', models.FloatField(null=True)),
                ('SNT', models.FloatField(null=True)),
                ('STORJ', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_transactions', to='api.Coin')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.Portfolio')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_transactions', to='api.Coin')),
            ],
        ),
        migrations.AddField(
            model_name='coin',
            name='portfolio',
            field=models.ManyToManyField(blank=True, related_name='coins', through='api.Position', to='api.Portfolio'),
        ),
    ]
