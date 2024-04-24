import pytest
from rates.exceptions import UnavailableTimeSpansError
from rates.serializers import PriceQueryParamsDeserializer, RateDeserializer


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
        """Ensures serializer is not valid when given time spans covers multiple days"""
        data = {
            "start": "2015-07-04T20:00:00+00:00",  # Saturday
            "end": "2015-07-08T20:00:00+00:00",  # Wednesday
        }
        deserializer = PriceQueryParamsDeserializer(data=data)

        assert deserializer.is_valid() is False
        assert (
            str(deserializer.errors["non_field_errors"][0])
            == UnavailableTimeSpansError.message
        )


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
        deserializer = RateDeserializer(data=data)
        assert deserializer.is_valid() is expectation

        if expectation is False:
            assert "times" in deserializer.errors
            assert (
                str(deserializer.errors["times"][0])
                == "Invalid time range format. Use '0600-1800' format"
            )
