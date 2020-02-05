from django.urls import path
from . import views


urlpatterns = [
    path("create-user/", views.CreateUser.as_view(), name="create user"),
    path("get-info/", views.UserHistoryInfo.as_view(), name="get user info"),
    path("transfer-money/", views.TransferMoney.as_view(), name="transfer money"),
]
