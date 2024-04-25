from django.urls import path

from rates.views import PriceListView
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register(r"parkingrates", PriceListView, basename="ParkingRate")


app_name = "rates"

urlpatterns = [
    path("price/", PriceListView.as_view({"get": "list"}), name="price-list"),
]
