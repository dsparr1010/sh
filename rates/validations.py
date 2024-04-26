import pytz
import re
from datetime import datetime
from typing import List
from django.core.exceptions import ValidationError

from rates.exceptions import UnavailableTimeSpansError


def validate_start_time_is_before_end_time(start_time: datetime, end_time: datetime):
    """Validates that the given start time occurs before the given end time"""
    if start_time >= end_time:
        raise ValidationError(
            {
                "start_time": f"The given end time {end_time} starts before the given start time {start_time}"
            }
        )


def validate_time_range_in_correct_format(times: str):
    pattern = r"^[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]$"
    if not re.match(pattern, times):
        raise ValidationError("Invalid time range format. Use '0600-1800' format")


def validate_time_range_spans_one_day(days_of_week: List):
    if days_of_week[0] != days_of_week[1]:
        raise UnavailableTimeSpansError


def validate_timezone_name_is_recognized(timezone: str):
    if timezone not in pytz.all_timezones_set:
        reference_link = (
            "https://gist.github.com/JellyWX/913dfc8b63d45192ad6cb54c829324ee"
        )
        raise ValidationError(
            f"Unrecognized timezone - please checkout {reference_link} for a list of acceptable timezones"
        )
