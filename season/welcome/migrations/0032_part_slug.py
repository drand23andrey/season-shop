# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0031_carouselelement_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
