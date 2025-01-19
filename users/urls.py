from django.urls import path
from .views import PaymentList

app_name = "users"

urlpatterns = [
    path("payments/", PaymentList.as_view(), name="payment-list"),
]