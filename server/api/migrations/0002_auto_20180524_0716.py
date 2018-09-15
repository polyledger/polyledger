# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-24 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='price',
        ),
        migrations.AddField(
            model_name='price',
            name='close',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='price',
            name='high',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='price',
            name='low',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='price',
            name='open',
            field=models.FloatField(default=0.0),
        ),
    ]