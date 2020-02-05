from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import transaction

from .serializers import CURRENCY_CHOICES


class UserProfile(AbstractUser):
    balance = models.FloatField()
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)

    def compare_emails(self, email):
        return True if self.email == email else False

    def enough_balance(self, amount):
        return True if self.balance > amount else False

    @classmethod
    def transfer_money(cls, from_user, to_user, amount):
        with transaction.atomic():
            from_user = cls.objects.select_for_update().get(email=from_user)
            to_user = cls.objects.select_for_update().get(email=to_user)

            if from_user.currency == to_user.currency:
                from_user.balance = round(from_user.balance - amount, 2)
                to_user.balance = round(to_user.balance + amount, 2)

                from_user.save()
                to_user.save()

                UserHistory.objects.create(user=from_user, event="write-off {} {}".format(amount, from_user.currency))
                UserHistory.objects.create(user=to_user, event="balance replenishment {} {}"
                                           .format(amount, to_user.currency))

            else:
                from_user.balance = round(from_user.balance - amount, 2)

                from_user_rate_to_base_currency = CurrencyRate.objects.get(currency=from_user.currency)
                to_user_rate_to_base_currency = CurrencyRate.objects.get(currency=to_user.currency)

                base_currency_money = round((1/from_user_rate_to_base_currency.rate)*amount, 2)
                to_user_money = round(base_currency_money / (1/to_user_rate_to_base_currency.rate), 2)

                to_user.balance = round(to_user.balance + to_user_money, 2)

                from_user.save()
                to_user.save()

                UserHistory.objects.create(user=from_user, event="write-off {} {}".format(amount, from_user.currency))
                UserHistory.objects.create(user=to_user, event="balance replenishment {} {}"
                                           .format(to_user_money, to_user.currency))


class UserHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)


class CurrencyRate(models.Model):
    rate = models.FloatField()
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3)