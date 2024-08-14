import pytest
from rates.models import ParkingRate
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime


class TestParkingRateModel:

    @pytest.mark.parametrize(
        "start_time,end_time,parking_rate_fixture",
        (
            (
                "2015-07-01T06:00:00-05:00",  # Wednesday 6am CST
                "2015-07-01T17:00:00-05:00",  # -> 5pm CST
                "parking_rate_mon_wed_sat",
            ),
            (
                "2015-07-03T10:00:00-06:00",  # Friday 10am EST
                "2015-07-03T15:00:00-06:00",  # -> 4pm EST
                "parking_rate_fri_sat_sun",
            ),
            (
                "2015-07-02T23:00:00+09:00",  # Thursday 11pm JST
                "2015-07-02T23:05:00+09:00",  # -> 11:05pm JST
                "parking_rate_mon_tues_thurs",
            ),
        ),
    )
    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_frame_returns_correct_instance(
        self, start_time, end_time, parking_rate_fixture, all_parking_rates, request
    ):
        """Test that expected rate instance is returned when filtered by day and times"""
        matching_rate_fixture = request.getfixturevalue(parking_rate_fixture)
        dt = get_format_with_datetime(start_time)
        start_dt = ParkingRateService.convert_timezone(dt)
        day = ParkingRateService.get_shorthand_weekday_name_by_number(dt)
        end_dt = get_format_with_datetime(end_time)
        end_dt_utc = ParkingRateService.convert_timezone(end_dt)

        res = ParkingRate.objects.filter_within_time_frame(
            start_time=start_dt, end_time=end_dt_utc, day=day
        )
        assert res.count() == 1
        assert res[0] == matching_rate_fixture
