# Generated by Django 4.2 on 2023-06-01 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackon_app', '0047_rename_nft_price_eth_geek_nft_price_tfuel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filteredassets',
            name='filtered_assets',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]