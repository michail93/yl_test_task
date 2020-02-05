from __future__ import absolute_import, unicode_literals

from django.conf import settings

from celery import task
import requests

from .models import CurrencyRate


@task()
def get_exchange_rates():
    result = requests.get(settings.EXCHANGE_RATES_API_URL)
    bitcoin_result = requests.get(settings.BITCOIN_EXCHANGE_RATES_API_URL)

    rates = result.json()["rates"]
    bitcoin_rate = bitcoin_result.json()

    for cur in rates:
        CurrencyRate.objects.update_or_create(currency=cur, defaults={"rate": rates[cur]})

    CurrencyRate.objects.update_or_create(currency="BTC", defaults={"rate": bitcoin_rate})

    print(rates)
    print({"BTC": bitcoin_rate})
