from datetime import datetime
import pytz
from django.db import models

from rates.exceptions import UnavailableTimeSpansError
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime


class ParkingRateManager(models.Manager):
    def filter_within_time_frame(self, start_time, end_time, day):
        results = self.filter_within_time_start_day_time(start_time=start_time, day=day)

        match len(results):
            case 0:
                # no applicable matches found
                raise UnavailableTimeSpansError
            case 1:
                # Only one was found - no need to filter deeper
                return results
            case _:
                return results.filter(end_time_utc__gte=end_time)

        # TODO: Keep until stable
        # otherwise, find overlap with given end time and original end time
        # applicable_rates_list = []

        # for rate in results:
        #     source_end_time = ParkingRateService.get_original_time_by_time_range(
        #         time_range=rate.original_time_range, specific_time="end"
        #     )
        #     source_tz = pytz.timezone(rate.original_given_timezone)
        #     end_time_as_given_tz = end_time.astimezone(source_tz)
        #     end_time_as_int = int(end_time_as_given_tz.time().strftime("%H%M"))

        #     if end_time_as_int <= int(source_end_time):
        #         applicable_rates_list.append(rate)

        # return applicable_rates_list

    def filter_within_time_start_day_time(self, day: str, start_time: datetime):
        return self.filter_by_day(day=day).filter(start_time_utc__lte=start_time)

    def filter_by_day(self, day):
        return self.get_queryset().filter(days__icontains=day)


class ParkingRate(models.Model):

    objects = ParkingRateManager()

    days = models.CharField(
        max_length=32,
        help_text="Shorthand days of the week that the rate applies to",
    )
    start_time_utc = models.TimeField(
        auto_now=False, auto_now_add=False, help_text="All times stored as UTC"
    )
    end_time_utc = models.TimeField(
        auto_now=False, auto_now_add=False, help_text="All times stored as UTC"
    )
    start_time_original = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        help_text="All times stored as the given tz upon ingestion",
    )
    end_time_original = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        help_text="All times stored as the given tz upon ingestion",
    )
    price = models.PositiveIntegerField(help_text="Prices in format 0000 in US Dollars")
    original_time_range = models.CharField(
        max_length=10, help_text="Original time range provided before conversion to UTC"
    )
    original_given_timezone = models.CharField(
        max_length=32, help_text="Timezone specified by owner"
    )
