# Generated by Django 4.2 on 2023-05-26 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackon_app', '0026_assets_floor_price_usd_assets_volume_traded_usd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assets',
            name='floor_price_usd',
        ),
        migrations.RemoveField(
            model_name='assets',
            name='volume_traded_usd',
        ),
        migrations.AddField(
            model_name='assets',
            name='floor_price_range',
            field=models.CharField(choices=[('0 - 50', '0 - 50'), ('50 -99', '50 -99'), ('100 - 999', '100 - 999'), ('1000 - 99999', '1000 - 99999'), ('99999 and Above', '99999 and Above'), ('None', 'None')], default='None', max_length=50),
        ),
        migrations.AddField(
            model_name='assets',
            name='volume_traded_range',
            field=models.CharField(choices=[('Below 10,000', 'Below 10,000'), ('10,000 - 99,999', '10,000 - 99,999'), ('100,000 - 999,999', '100,000 - 999,999'), ('1,000,000 - 49,999,999', '1,000,000 - 49,999,999'), ('50,000,000 - 499,999,999', '50,000,000 - 499,999,999'), ('500,000,000 - 999,999,999', '500,000,000 - 999,999,999'), ('1,000,000,000 and Above', '1,000,000,000 and Above'), ('None', 'None')], default='None', max_length=50),
        ),
    ]
