# Generated by Django 3.0.2 on 2020-01-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money_transfer_system', '0004_auto_20200129_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('currency', models.CharField(choices=[('EUR', 'Euro'), ('USD', 'United States dollars'), ('GPB', 'Pound sterling'), ('RUB', 'Russian ruble'), ('BTC', 'Bitcoin')], max_length=3)),
            ],
        ),
    ]
