from datetime import datetime
from django.db import models
from rates.exceptions import UnavailableTimeSpansError


class ParkingRateManager(models.Manager):

    def filter_within_time_frame(
        self, start_time: datetime, end_time: datetime, day: str
    ):
        """Query for rates within a day and time range"""

        end_time_query_construction = (
            "end_time_utc__lte" if start_time < end_time else "end_time_utc__gte"
        )
        end_time_query = {end_time_query_construction: end_time}

        results = self.get_queryset().filter(
            days__icontains=day,
            start_time_utc__lte=start_time,
            **end_time_query,
        )

        match len(results):
            case 0:
                # no applicable matches found
                raise UnavailableTimeSpansError
            case _:
                return results


class ParkingRate(models.Model):

    objects = ParkingRateManager()

    days = models.CharField(
        max_length=32,
        help_text="Shorthand days of the week that the rate applies to",
        db_index=True,
    )
    start_time_utc = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        help_text="All times stored as UTC",
        db_index=True,
    )
    end_time_utc = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        help_text="All times stored as UTC",
        db_index=True,
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

    unique_together = ("days", "start_time_utc", "end_time_utc")
