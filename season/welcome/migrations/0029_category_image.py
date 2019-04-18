# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-16 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import welcome.models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0028_auto_20190416_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to=welcome.models.image_folder),
            preserve_default=False,
        ),
    ]
