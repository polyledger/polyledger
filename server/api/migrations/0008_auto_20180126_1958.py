# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-26 19:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180124_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(db_index=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'IP Address',
                'verbose_name_plural': 'IP Addresses',
            },
        ),
        migrations.AddField(
            model_name='distribution',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
