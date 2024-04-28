import pytest
from contextlib import nullcontext as does_not_raise
from datetime import datetime
from django.core.exceptions import ValidationError
from rates.exceptions import UnavailableTimeSpansError
from rates.validations import (
    validate_start_time_is_before_end_time,
    validate_time_range_in_correct_format,
    validate_time_range_spans_one_day,
)


class TestValidateStartAndEndTimes:

    @pytest.mark.parametrize(
        "start_time,end_time,expectation",
        (
            (
                "2015-07-04T20:00:00+00:00",
                "2015-07-04T15:00:00+00:00",
                pytest.raises(ValidationError),
            ),
            (
                "2015-07-01T12:00:00-05:00",
                "2015-07-01T07:00:00-05:00",
                pytest.raises(ValidationError),
            ),
            (
                "2015-07-04T15:00:00+00:00",
                "2015-07-04T20:00:00+00:00",
                does_not_raise(),
            ),
            (
                "2015-07-01T07:00:00-05:00",
                "2015-07-01T12:00:00-05:00",
                does_not_raise(),
            ),
        ),
    )
    def test_validate_start_time_is_before_end_time(
        self, start_time, end_time, expectation
    ):
        """Ensures validation raises error when the given start time occurs before the given end time"""
        with expectation:
            validate_start_time_is_before_end_time(
                start_time=datetime.fromisoformat(start_time),
                end_time=datetime.fromisoformat(end_time),
            )

    @pytest.mark.parametrize(
        "time_range,expectation",
        (
            (
                "6:00-9:30",
                pytest.raises(ValidationError),
            ),
            (
                "600-900",
                pytest.raises(ValidationError),
            ),
            (
                "0600-0900",
                does_not_raise(),
            ),
            (
                "1600-2000",
                does_not_raise(),
            ),
        ),
    )
    def test_validate_time_range_in_correct_format(self, time_range, expectation):
        """Ensure validation raises error if time range is not in correct format"""
        with expectation:
            validate_time_range_in_correct_format(times=time_range)

    @pytest.mark.parametrize(
        "days_list,expectation",
        (
            (["sat", "sun"], pytest.raises(UnavailableTimeSpansError)),
            (["sun", "wed"], pytest.raises(UnavailableTimeSpansError)),
            (["mon", "mon"], does_not_raise()),
            (["tues", "tues"], does_not_raise()),
        ),
    )
    def test_validate_time_range_spans_one_day(self, days_list, expectation):
        """Ensure a time span does not range across multiple days"""
        with expectation:
            validate_time_range_spans_one_day(days_of_week=days_list)
