from django.db import models

from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime


class ParkingRateManager(models.Manager):
    def filter_within_time_frame(self, start_time, end_time):

        end_time_constraint = (
            "end_time__lte" if start_time < end_time else "end_time__gte"
        )

        filter_by = {"start_time__gte": start_time, end_time_constraint: end_time}
        return self.get_queryset().filter(**filter_by)

    def filter_by_day(self, day):
        return self.get_queryset().filter(days__icontains=day)

    def filter_by_day_and_time(self, start, end):
        start_dt = get_format_with_datetime(iso_datetime=start)
        start_time_utc = ParkingRateService().convert_timezone_to_utc(start_dt)
        end_dt = get_format_with_datetime(iso_datetime=end)
        end_time_utc = ParkingRateService().convert_timezone_to_utc(end_dt)

        date = ParkingRateService().get_shorthand_weekday_name_by_number(
            iso_format=start_time_utc
        )

        check = self.get_queryset().filter(
            start_time__gte=start_time_utc,
            start_time__lte=end_time_utc,
            days__icontains=date,
        )

        print(check)


class ParkingRate(models.Model):

    objects = ParkingRateManager()

    days = models.CharField(
        max_length=32,
        help_text="Shorthand days of the week that the rate applies to",
    )
    start_time = models.TimeField(
        auto_now=False, auto_now_add=False, help_text="All times stored as UTC"
    )
    end_time = models.TimeField(
        auto_now=False, auto_now_add=False, help_text="All times stored as UTC"
    )
    price = models.PositiveIntegerField(help_text="Prices in format 0000 in US Dollars")
    original_time_range = models.CharField(
        max_length=10, help_text="Original time range provided before conversion to UTC"
    )
    original_given_timezone = models.CharField(
        max_length=32, help_text="Timezone specified by owner"
    )
