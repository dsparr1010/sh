from datetime import datetime
import pytest
from rates.models import ParkingRate
from rates.utils import get_format_with_datetime


class TestParkingRate:

    @pytest.mark.parametrize(
        "parking_rate_fixture,search_term",
        (("parking_rate_wed", "wed"), ("parking_rate_mon_tues_thurs", "tues")),
    )
    @pytest.mark.django_db(transaction=True)
    def test_filter_by_day(self, parking_rate_fixture, search_term, request):
        fixture_instance = request.getfixturevalue(parking_rate_fixture)
        instance = ParkingRate.objects.filter_by_day(day=search_term)
        assert instance.count() == 1
        assert search_term in instance[0].days
        assert fixture_instance == instance[0]

    @pytest.mark.django_db(transaction=True)
    def test_filter_within_time_frame(self, all_parking_rates):
        start_dt = get_format_with_datetime(
            iso_datetime="2015-07-04T14:00:00+00:00"
        ).time()
        end_dt = get_format_with_datetime(
            iso_datetime="2015-07-04T20:00:00+00:00"
        ).time()

        check = ParkingRate.objects.all()

        for x in check:
            print(x)
            print(f"start: {x.start_time}")
            print(f"end: {x.end_time}")

        instances = ParkingRate.objects.filter_within_time_frame(
            start_time=start_dt, end_time=end_dt
        )

        for x in instances:
            print(x)

    @pytest.mark.django_db(transaction=True)
    def test_filter_by_day_and_time(self, all_parking_rates):
        pass
