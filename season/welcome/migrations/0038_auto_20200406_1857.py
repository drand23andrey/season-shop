# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-04-06 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0037_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='part',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='welcome.Category'),
        ),
    ]
