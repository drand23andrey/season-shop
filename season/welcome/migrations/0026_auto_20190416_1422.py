# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-16 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0025_auto_20190404_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Принят в обработку', 'Принят в обработку'), ('Ожидает оплаты', 'Ожидает оплаты'), ('Оплачен, выполняется', 'Оплачен, выполняется'), ('Выполнен', 'Выполнен')], default='Принят в обработку', max_length=100),
        ),
    ]