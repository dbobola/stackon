# Generated by Django 4.2 on 2023-05-31 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackon_app', '0046_rename_discordmodcollectioncontractabi_contract_stackonmodcollectioncontractabi_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geek',
            old_name='nft_price_eth',
            new_name='nft_price_tfuel',
        ),
        migrations.AddField(
            model_name='geek',
            name='nft_minting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='geek',
            name='nft_total_supply',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='geek',
            name='nft_status',
            field=models.CharField(choices=[('geeks', 'Geeks'), ('modifiers', 'Modifiers'), ('stackon-bots', 'Stackon Bots')], default='geeks', max_length=100),
        ),
    ]