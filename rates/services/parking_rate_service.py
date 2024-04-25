from typing import Optional, Union
import pytz

from datetime import datetime

from rates.exceptions import UnavailableTimeSpansError
from rates.utils import get_format_with_datetime


class ParkingRateInfo:
    DAYS: str
    TIMES: str
    TIMEZONE: str
    PRICE: int


class ParkingRateService:
    STANDARDIZED_TIME = pytz.utc  # Convert all times given from requests to UTC
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

    DAYS_OF_WEEK = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]

    def _format_datetime(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S%z")

    def get_shorthand_weekday_name_by_number(self, iso_format: datetime):
        return self.DAYS_OF_WEEK[iso_format.weekday()]

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

    def get_rates_within_datetimes(self, start: str, end: str):
        from rates.models import ParkingRate

        iso_start_dt = get_format_with_datetime(start)
        start_dt = self.convert_timezone_to_utc(iso_start_dt)
        day = self.get_shorthand_weekday_name_by_number(start_dt)
        end_dt = get_format_with_datetime(end)

        results = ParkingRate.objects.filter_within_time_frame(
            start_time=start_dt, end_time=end_dt, day=day
        )

        match len(results):
            case 0:
                raise UnavailableTimeSpansError
            case _:
                return results

    def convert_timezone_to_utc(self, datetime_obj: datetime):
        """Convert a datetime object to UTC"""
        source_tz = datetime_obj.tzname()

        if source_tz == self.STANDARDIZED_TIME:
            return datetime_obj

        # return self._format_datetime(datetime_obj.astimezone(self.STANDARDIZED_TIME))
        return datetime_obj.astimezone(self.STANDARDIZED_TIME)

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
