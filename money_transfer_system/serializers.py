from django.conf import settings

from rest_framework import serializers


CURRENCY_CHOICES = [
    ("EUR", "Euro"),
    ("USD", "United States dollars"),
    ("GBP", "Pound sterling"),
    ("RUB", "Russian ruble"),
    ("BTC", "Bitcoin")
]


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    balance = serializers.FloatField(min_value=1)
    currency = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    password = serializers.CharField(max_length=30)


class UserInfo(serializers.Serializer):
    event = serializers.CharField(max_length=200)
    date = serializers.DateTimeField(format=settings.REST_DATETIME_FORMAT)


class TransferMoneySerializer(serializers.Serializer):
    transaction_email = serializers.EmailField(max_length=150)
    amount = serializers.FloatField(min_value=1)
