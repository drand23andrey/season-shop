# Generated by Django 3.0.5 on 2020-04-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0005_auto_20200416_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselelement',
            name='link',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
