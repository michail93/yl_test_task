import json
import base64

from django.test import TestCase

from .models import UserHistory, UserProfile, CurrencyRate


class MoneyTransferSystemTestCase(TestCase):
    def setUp(self):
        self.BASE_CURRENCY = "RUB"

        rates = {
            "EUR": 0.0141645467,
            "RUB": 1.0,
            "USD": 0.0156744874,
            "GBP": 0.0120079945,
            "BTC": 1.71e-06
        }

        for cur in rates:
            CurrencyRate.objects.update_or_create(currency=cur, defaults={"rate": rates[cur]})

        self.user1_data = {
            "email": "mark@mark.com",
            "balance": 360,
            "currency": "EUR",
            "password": "test"
        }

        self.user2_data = {
            "email": "tom@tom.com",
            "balance": 52,
            "currency": "GBP",
            "password": "test"
        }

        self.request_data = {
            "transaction_email": "tom@tom.com",
            "amount": 10.14
        }

        email_password_string = "{}:{}".format(self.user1_data["email"], self.user1_data["password"])

        self.credentials = base64.b64encode(email_password_string.encode()).decode('ascii')

    def test_create_user(self):
        user_data = {
            "email": "petr@petr.com",
            "balance": 126,
            "currency": "RUB",
            "password": "test"
        }

        response = self.client.post('/money-transfer/create-user/', data=json.dumps(user_data),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)

        new_response = self.client.post('/money-transfer/create-user/', data=json.dumps(user_data),
                                        content_type="application/json")

        self.assertEqual(new_response.status_code, 409)

    def test_success_transfer_money(self):

        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user1_data),
                         content_type="application/json")

        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user2_data),
                         content_type="application/json")

        user1_data_balance = 349.86
        user2_data_balance = 60.6

        response = self.client.post('/money-transfer/transfer-money/', data=json.dumps(self.request_data),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Basic {}".format(self.credentials))

        self.assertEqual(response.status_code, 200)

        user1 = UserProfile.objects.get(email=self.user1_data["email"])
        user2 = UserProfile.objects.get(email=self.user2_data["email"])

        self.assertEqual(user1.balance, user1_data_balance)
        self.assertEqual(user2.balance, user2_data_balance)

    def test_not_enough_balance(self):
        request_data = {
            "transaction_email": "tom@tom.com",
            "amount": 1000
        }

        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user1_data),
                         content_type="application/json")

        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user2_data),
                         content_type="application/json")

        response = self.client.post('/money-transfer/transfer-money/', data=json.dumps(request_data),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Basic {}".format(self.credentials))

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["response"], "not enough balance")

    def test_user_not_found(self):
        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user1_data),
                         content_type="application/json")

        response = self.client.post('/money-transfer/transfer-money/', data=json.dumps(self.request_data),
                                    content_type="application/json",
                                    HTTP_AUTHORIZATION="Basic {}".format(self.credentials))

        self.assertEqual(response.status_code, 404)

    def test_user_history(self):
        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user1_data),
                         content_type="application/json")

        self.client.post('/money-transfer/create-user/', data=json.dumps(self.user2_data),
                         content_type="application/json")

        self.client.post('/money-transfer/transfer-money/', data=json.dumps(self.request_data),
                         content_type="application/json",
                         HTTP_AUTHORIZATION="Basic {}".format(self.credentials))

        user1 = UserProfile.objects.get(email=self.user1_data["email"])
        user2 = UserProfile.objects.get(email=self.user2_data["email"])

        user1_history = UserHistory.objects.get(user=user1)
        user2_history = UserHistory.objects.get(user=user2)

        self.assertEqual(user1_history.event, "write-off {} {}".format(self.request_data["amount"], user1.currency))
        self.assertEqual(user2_history.event, "balance replenishment {} {}".format(8.6, user2.currency))
