import datetime
import pytest
from rates.models import ParkingRate
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime


class TestParkingRate:

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
        request.getfixturevalue(parking_rate_fixture)
        instance = ParkingRate.objects.filter_by_day(day=search_term)
        assert instance.count() == count
        assert search_term in instance[0].days

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_start_day_time_returns_correct_instance(
        self, all_parking_rates
    ):
        dt = get_format_with_datetime("2015-07-01T07:00:00-05:00")
        start_dt = ParkingRateService().convert_timezone_to_utc(dt)
        day = ParkingRateService().get_shorthand_weekday_name_by_number(dt)
        res = ParkingRate.objects.filter_within_time_start_day_time(
            start_time=start_dt, day=day
        )
        assert len(res) == 1
        assert day in res[0].days

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_start_day_time_finds_no_applicable_instances(
        self, parking_rate_wed
    ):
        """
        Test that a start time of 5:00am CST on Wednesday yields no results
        Only start times after 6:00am CST on Wednesday would yield 1 result
        """
        dt = get_format_with_datetime("2015-07-01T05:00:00-05:00")
        start_dt = ParkingRateService().convert_timezone_to_utc(dt)
        day = ParkingRateService().get_shorthand_weekday_name_by_number(dt)
        res = ParkingRate.objects.filter_within_time_start_day_time(
            start_time=start_dt, day=day
        )
        assert res.count() == 0

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_start_day_time_returns_correct_instance(
        self, all_parking_rates
    ):
        dt = get_format_with_datetime("2015-07-01T06:00:00-05:00")
        start_dt = ParkingRateService().convert_timezone_to_utc(dt)
        day = ParkingRateService().get_shorthand_weekday_name_by_number(dt)
        dt = get_format_with_datetime("2015-07-01T17:00:00-05:00")
        end_dt = datetime.datetime.fromisoformat("2015-07-01T17:00:00-05:00")

        res = ParkingRate.objects.filter_within_time_frame(
            start_time=start_dt, end_time=end_dt, day=day
        )
        assert len(res) == 1
        assert day in res[0].days

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_start_day_time_returns_multiple_correct_instance(
        self, all_parking_rates
    ):
        dt = get_format_with_datetime("2015-07-01T06:00:00-05:00")
        start_dt = ParkingRateService().convert_timezone_to_utc(dt)
        day = ParkingRateService().get_shorthand_weekday_name_by_number(dt)
        end_dt = datetime.datetime.fromisoformat("2015-07-01T17:00:00-05:00")

        res = ParkingRate.objects.filter_within_time_frame(
            start_time=start_dt, end_time=end_dt, day=day
        )
        assert len(res) == 1
        assert day in res[0].days
