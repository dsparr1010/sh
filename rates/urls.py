from django.urls import path

from rates.views import PriceListView


app_name = "rates"

urlpatterns = [
    path("price/", PriceListView.as_view(), name="price-list"),
]
