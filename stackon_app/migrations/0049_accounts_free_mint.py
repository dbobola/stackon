# Generated by Django 4.2 on 2023-06-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackon_app', '0048_alter_filteredassets_filtered_assets'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='free_mint',
            field=models.IntegerField(default=0),
        ),
    ]