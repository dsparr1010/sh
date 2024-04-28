import pytest
from rates.exceptions import UnavailableTimeSpansError
from rates.serializers import (
    PriceQueryParamsDeserializer,
    RateDeserializer,
    RateSerializer,
)


class TestPriceQueryParamsDeserializer:

    @pytest.mark.parametrize(
        "start_time,end_time,expectation",
        (
            ("2015-07-04T20:00:00+00:00", "2015-07-04T15:00:00+00:00", False),
            ("2015-07-01T12:00:00-05:00", "2015-07-01T07:00:00-05:00", False),
            ("2015-07-04T15:00:00+00:00", "2015-07-04T20:00:00+00:00", True),
            ("2015-07-01T07:00:00-05:00", "2015-07-01T12:00:00-05:00", True),
        ),
    )
    def test_validate_start_time_is_before_end_time(
        self, start_time, end_time, expectation
    ):
        """Ensures serializer is not valid when the given start time occurs before the given end time"""
        data = {"start": start_time, "end": end_time}
        deserializer = PriceQueryParamsDeserializer(data=data)
        assert deserializer.is_valid() is expectation

        if expectation is False:
            assert "start_time" in deserializer.errors
            assert deserializer.errors["start_time"][0].code == "invalid"

    def test_validate_days_of_week(self):
        """
        Ensures serializer is not valid and raises UnavailableTimeSpansError
        when given time spans covers multiple days
        """
        data = {
            "start": "2015-07-04T20:00:00+00:00",  # Saturday
            "end": "2015-07-08T20:00:00+00:00",  # Wednesday
        }
        deserializer = PriceQueryParamsDeserializer(data=data)

        with pytest.raises(UnavailableTimeSpansError):
            assert deserializer.is_valid() is False


class TestRateDeserializer:

    @pytest.mark.parametrize(
        "time_range,expectation",
        (
            ("6:00-9:30", False),
            ("600-900", False),
            ("0600-0900", True),
            ("1600-2000", True),
        ),
    )
    def test_validate_time_range(self, time_range, expectation):
        data = {
            "days": "mon,tue,wed",
            "times": time_range,
            "tz": "America/Chicago",
            "price": 1000,
        }
        """Test that format for 'times' is strictly enforced"""
        deserializer = RateDeserializer(data=data)
        assert deserializer.is_valid() is expectation

        if expectation is False:
            assert "times" in deserializer.errors
            assert (
                str(deserializer.errors["times"][0])
                == "Invalid time range format. Use '0600-1800' format"
            )


class TestRateSerializer:
    expected_fields = {"days", "times", "tz", "price"}

    @pytest.mark.django_db(transaction=True)
    def test_expected_fields_are_returned(self, parking_rate_fri_sat_sun):
        """Test that expected keys are returned from serializer"""
        data = {
            "times": parking_rate_fri_sat_sun.original_time_range,
            "tz": parking_rate_fri_sat_sun.original_given_timezone,
            "days": parking_rate_fri_sat_sun.days,
            "price": parking_rate_fri_sat_sun.price,
        }
        serializer = RateSerializer(data=data)
        serializer.is_valid()
        assert all(field in serializer.data.keys() for field in self.expected_fields)


class TestPriceSerializer:
    expected_field = "price"

    @pytest.mark.django_db(transaction=True)
    def test_expected_fields_are_returned(self, parking_rate_fri_sat_sun):
        """Test that expected key is returned from serializer"""
        data = {
            "price": parking_rate_fri_sat_sun.price,
        }
        serializer = RateSerializer(data=data)
        serializer.is_valid()
        assert self.expected_field in serializer.data.keys()
