from django.urls import path
from rates.views import PriceListView, RatesListView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"parkingrates", PriceListView, basename="ParkingRate")


app_name = "rates"

urlpatterns = [
    path("price/", PriceListView.as_view({"get": "list"}), name="price-list"),
    path(
        "rates/",
        RatesListView.as_view({"get": "list", "put": "update"}),
        name="rates-list",
    ),
]
