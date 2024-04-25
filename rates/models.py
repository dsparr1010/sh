from django.db import models

from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime


class ParkingRateManager(models.Manager):
    def filter_within_time_frame(self, start_time, end_time, day):
        results = self.filter_within_time_start_day_time(start_time=start_time, day=day)

        # return early if no results were found
        if len(results) == 0:
            return results

        # otherwise, find overlap with given end time and original end time
        end_time_int = int(end_time.time().strftime("%H%M"))
        applicable_rates_list = []

        for rate in results:
            original_end_time = ParkingRateService.get_original_time_by_time_range(
                time_range=rate.original_time_range, specific_time="end"
            )
            if end_time_int <= int(original_end_time):
                applicable_rates_list.append(rate)

        return applicable_rates_list

    def filter_within_time_start_day_time(self, day, start_time):
        return self.filter_by_day(day=day).filter(start_time__lte=start_time)

    def filter_by_day(self, day):
        return self.get_queryset().filter(days__icontains=day)


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
