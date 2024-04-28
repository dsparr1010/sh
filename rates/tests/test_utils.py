import pytest
from datetime import datetime
from rates.models import ParkingRate
from rates.seed import seed_database_with_parking_rates
from rates.utils import get_format_with_datetime, replace_space_w_plus


class TestUtils:

    @pytest.mark.parametrize(
        "iso_format", ("2015-07-01T07:00:00 05:00", "2015-07-04T15:00:00+00:00")
    )
    def test_get_format_with_datetime(self, iso_format):
        """Test that a datetime object is returned from an ISO-8601 formatted string"""
        iso_dt = get_format_with_datetime(iso_format)
        assert isinstance(iso_dt, datetime)

    @pytest.mark.parametrize(
        "missing_plus,expectation",
        (
            ("2015-07-01T07:00:00 05:00", "2015-07-01T07:00:00+05:00"),
            ("2015-07-04T15:00:00 00:00", "2015-07-04T15:00:00+00:00"),
        ),
    )
    def test_replace_space_w_plus(self, missing_plus, expectation):
        """Test that spaces in string is replaced by '+'"""
        assert replace_space_w_plus(string_dt=missing_plus) == expectation


class TestSeed:
    """Tests for 'seed_database_with_parking_rates'"""

    @pytest.mark.django_db(transaction=True)
    def test_rate_config_ready_seeds_db(self):
        """Ensure calling seeding function results in objects in the database"""

        assert ParkingRate.objects.all().count() == 0

        seed_database_with_parking_rates()

        seeded_instances = ParkingRate.objects.all()
        assert seeded_instances.count() == 5
