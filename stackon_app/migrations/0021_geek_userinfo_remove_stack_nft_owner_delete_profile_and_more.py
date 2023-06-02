# Generated by Django 4.2 on 2023-05-23 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stackon_app', '0020_stack_nft_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nft_status', models.CharField(choices=[('Owned', 'Owned'), ('Borrowed', 'Borrowed'), ('Public', 'Public')], default='Public', max_length=8)),
                ('nft_name', models.CharField(default='null', max_length=255)),
                ('nft_image', models.CharField(blank=True, max_length=100, null=True)),
                ('nft_seller', models.CharField(default='logo.ico', max_length=100)),
                ('nft_description', models.TextField(blank=True, null=True)),
                ('nft_price_eth', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nft_price_usd', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_avatar', models.CharField(max_length=100)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('equity_eth', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('equity_usd', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('equity_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('equity_base', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('next_1d_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('next_2d_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('next_3d_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('next_7d_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('next_14d_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('next_30d_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('active_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('stack', models.ManyToManyField(to='stackon_app.nftasset')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='stack',
            name='nft_owner',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Stack',
        ),
    ]
