# Generated by Django 4.2 on 2023-05-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackon_app', '0028_assets_trend_percent_alter_assets_floor_price_range_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='blockchain_logo',
            field=models.CharField(default='eth-logo.svg', max_length=100),
        ),
    ]