# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-03 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0023_auto_20190403_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='welcome.Cart'),
        ),
    ]
