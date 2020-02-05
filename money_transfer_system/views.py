from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from . import serializers
from .models import UserProfile, UserHistory


class CreateUser(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.CreateUserSerializer

    def post(self, request, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if UserProfile.objects.filter(username=serializer.data["email"]).exists():
            return Response(status=status.HTTP_409_CONFLICT,
                            data={"response": "User with email {} already exists".format(serializer.data["email"])})

        user = UserProfile.objects.create_user(username=serializer.data["email"], email=serializer.data["email"],
                                               balance=round(serializer.data["balance"], 2),
                                               currency=serializer.data["currency"],
                                               password=serializer.data["password"])

        request.data.pop("password")

        return Response(data={"data is": request.data}, status=status.HTTP_201_CREATED)


class UserHistoryInfo(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        qs = UserHistory.objects.filter(user=request.user).order_by("date")
        serializer = serializers.UserInfo(qs, many=True)
        return Response(data=serializer.data)


class TransferMoney(generics.GenericAPIView):
    serializer_class = serializers.TransferMoneySerializer

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.data["amount"]
        transaction_email = serializer.data["transaction_email"]

        if not UserProfile.objects.filter(email=transaction_email).exists():
            return Response(data={"response": "user with email {} is not found!".format(transaction_email)},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user.compare_emails(transaction_email):
            return Response(data={"response": "addressed email {} is email of user".format(transaction_email)},
                            status=status.HTTP_409_CONFLICT)

        if not request.user.enough_balance(amount):
            return Response(data={"response": "not enough balance"}, status=status.HTTP_409_CONFLICT)

        request.user.transfer_money(request.user.email, transaction_email, amount)

        response_data = serializer.data

        response_data.update({"currency": request.user.currency})

        return Response(data=response_data)
