import pytz

from datetime import datetime


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

    def convert_timezone_to_utc(self, datetime_obj: datetime):
        """Convert a datetime object to UTC"""
        source_tz = datetime_obj.tzname()

        if source_tz == "UTC":
            return self._format_datetime(datetime_obj)

        return self._format_datetime(datetime_obj.astimezone(self.STANDARDIZED_TIME))

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
