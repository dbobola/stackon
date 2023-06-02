# Generated by Django 4.2 on 2023-05-31 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackon_app', '0044_accounts_private_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_private_key', models.TextField(blank=True)),
                ('admin_wallet_address', models.TextField(blank=True)),
                ('twitterModCollectionContractAddress', models.TextField(blank=True)),
                ('telegramModCollectionContractAddress', models.TextField(blank=True)),
                ('discordModCollectionContractAddress', models.TextField(blank=True)),
                ('redditModCollectionContractAddress', models.TextField(blank=True)),
                ('overallModCollectionContractAddress', models.TextField(blank=True)),
                ('twitterModCollectionContractABI', models.JSONField(blank=True)),
                ('telegramModCollectionContractABI', models.JSONField(blank=True)),
                ('discordModCollectionContractABI', models.JSONField(blank=True)),
                ('redditModCollectionContractABI', models.JSONField(blank=True)),
                ('overallModCollectionContractABI', models.JSONField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='filteredassets',
            name='filtered_assets',
            field=models.JSONField(blank=True),
        ),
    ]
