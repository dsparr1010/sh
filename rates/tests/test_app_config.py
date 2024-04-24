from django.test import TestCase
from django.apps import apps
from rates.apps import RatesConfig
from rates.models import ParkingRate


class RatesConfigTests(TestCase):

    def test_config_is_registered(self):
        """Ensure RatesConfig is correctly registered"""
        rates_config = apps.get_app_config("rates")
        assert rates_config.name == "rates"
        assert rates_config.verbose_name == "Parking Rates"
        assert isinstance(rates_config, RatesConfig)

    def test_rate_config_ready_seeds_db(self):
        """Ensure calling RatesConfig.ready() seeds (class) ParkingRate table"""

        RatesConfig(app_name="rates", app_module="rates.apps.RatesConfig").ready()

        seeded_instances = ParkingRate.objects.all()
        assert seeded_instances.count() == 5
