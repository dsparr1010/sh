import factory
from rates.models import ParkingRate


class ParkingRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParkingRate
