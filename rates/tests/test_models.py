import pytest
from rates.models import ParkingRate
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime


class TestParkingRateModel:

    @pytest.mark.parametrize(
        "parking_rate_fixture,search_term,count",
        (
            ("parking_rate_wed", "wed", 1),
            ("parking_rate_mon_tues_thurs", "tues", 1),
            ("all_parking_rates", "wed", 2),
        ),
    )
    @pytest.mark.django_db(transaction=True)
    def test_filter_by_day(self, parking_rate_fixture, search_term, count, request):
        """Test that correct number of results are returned when filtering by day of the week"""
        request.getfixturevalue(parking_rate_fixture)
        instance = ParkingRate.objects.filter_by_day(day=search_term)
        assert instance.count() == count
        assert search_term in instance[0].days

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_start_day_time_returns_correct_instance(
        self, all_parking_rates, parking_rate_mon_wed_sat
    ):
        """Test that filtering within a given datetime's day and start time return correct results"""
        dt = get_format_with_datetime("2015-07-01T01:00:00-05:00")  # Wednesday 1am CST
        start_dt = ParkingRateService.convert_timezone(dt)  # Converts to 6am UTC time

        day = ParkingRateService.get_shorthand_weekday_name_by_number(dt)
        res = ParkingRate.objects.filter_within_time_start_day_time(
            start_time=start_dt, day=day
        )

        assert res.count() == 1  # Only one applicable rate found
        assert day in res[0].days
        assert (
            res[0] == parking_rate_mon_wed_sat
        )  # One rate found should be equal to this instance

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_start_day_time_finds_no_applicable_instances(
        self, parking_rate_wed
    ):
        """
        Test that a start time of 5:00am CST on Wednesday yields no results
        Only start times after 6:00am CST on Wednesday would yield 1 result
        """
        dt = get_format_with_datetime("2015-07-01T05:00:00-05:00")
        start_dt = ParkingRateService.convert_timezone(dt)
        day = ParkingRateService().get_shorthand_weekday_name_by_number(dt)
        res = ParkingRate.objects.filter_within_time_start_day_time(
            start_time=start_dt, day=day
        )
        assert res.count() == 0

    @pytest.mark.parametrize(
        "start_time,end_time,parking_rate_fixture",
        (
            (
                "2015-07-01T06:00:00-05:00",  # Wednesday 6am CST
                "2015-07-01T17:00:00-05:00",  # -> 5pm CST
                "parking_rate_wed",
            ),
            (
                "2015-07-03T10:00:00-06:00",  # Friday 10am EST
                "2015-07-03T19:00:00-06:00",  # -> 7pm EST
                "parking_rate_fri_sat_sun",
            ),
            (
                "2015-07-02T23:00:00+09:00",  # Thursday 11pm JST
                "2015-07-02T02:00:00+09:00",  # -> 12pm JST
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
