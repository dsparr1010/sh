from typing import Optional, Union
import pytz
from django.db.models import Q

from datetime import datetime

from rates.exceptions import NoInstanceFound, NothingToUpdate, UnavailableTimeSpansError
from rates.utils import get_format_with_datetime


class ParkingRateService:
    STANDARDIZED_TIME = pytz.utc  # Convert all times given from requests to UTC
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

    def _format_datetime(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S%z")

    @staticmethod
    def get_shorthand_weekday_name_by_number(iso_format: datetime):
        DAYS_OF_WEEK = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]
        return DAYS_OF_WEEK[iso_format.weekday()]

    @staticmethod
    def get_original_time_by_time_range(
        time_range: str, specific_time: Optional[Union[int, str]]
    ) -> str:
        """Get the original time range, returning start, end, or both times"""
        split_range = time_range.split("-", 2)
        match specific_time:
            case "start" | 0:
                return split_range[0]
            case "end" | 1:
                return split_range[1]
            case _:
                return split_range

    @classmethod
    def get_rates_within_datetimes(cls, start: str, end: str):
        from rates.models import ParkingRate

        iso_start_dt = get_format_with_datetime(start)
        start_dt_utc = cls.convert_timezone(iso_start_dt)
        day = cls.get_shorthand_weekday_name_by_number(start_dt_utc)
        end_dt = get_format_with_datetime(end)
        end_dt_utc = cls.convert_timezone(end_dt)

        results = ParkingRate.objects.filter_within_time_frame(
            start_time=start_dt_utc, end_time=end_dt_utc, day=day
        )

        match len(results):
            case 0:
                raise UnavailableTimeSpansError
            case _:
                return results

    @classmethod
    def update_rate_instance(cls, days, start_time_utc, end_time_utc, price, **kwargs):
        from rates.models import ParkingRate

        try:
            result = ParkingRate.objects.filter_within_time_frame(
                start_time=start_time_utc, end_time=end_time_utc, day=days
            ).first()

            if result.price == price:
                # Nothing to update - request body matches existing instance
                raise NothingToUpdate

            # Otherwise, update price
            result.price = price
            result.save()

            return result
        except UnavailableTimeSpansError as err:
            # If there is no instance found, then there is nothing to update
            raise NoInstanceFound from err

    @staticmethod
    def convert_timezone(datetime_obj: datetime, timezone: str = "UTC"):
        """Convert a datetime object to the given timezone"""
        source_tz = datetime_obj.tzname()
        target_timezone = pytz.timezone(timezone)

        if source_tz == target_timezone:
            return datetime

        return datetime_obj.astimezone(target_timezone)

    def convert_plain_text_time_tz_to_utc(self, time: str, tz: str):
        given_timezone = pytz.timezone(tz)
        # Arbitrarily setting choosing a date so we can create a dummy datetime object
        date = datetime(1991, 10, 10, 0, 0, 0)
        datetime_str = f"{date.date()} {time}"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H%M")
        localized_time = given_timezone.localize(datetime_obj)

        # Convert given time and locale to UTC
        return (
            localized_time.astimezone(self.STANDARDIZED_TIME)
            .time()
            .strftime("%H:%M:%S")
        )
