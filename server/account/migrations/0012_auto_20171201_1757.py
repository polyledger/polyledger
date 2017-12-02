# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-02 01:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20171201_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='coin',
            name='percent',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='coins',
        ),
        migrations.AddField(
            model_name='allocation',
            name='coin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Coin'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='allocations',
            field=models.ManyToManyField(to='account.Allocation'),
        ),
    ]
