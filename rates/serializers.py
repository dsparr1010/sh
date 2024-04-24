from rates.services.parking_rate_service import ParkingRateService
from rates.validations import (
    validate_start_time_is_before_end_time,
    validate_time_range_in_correct_format,
    validate_time_range_spans_one_day,
    validate_timezone_name_is_recognized,
)
from django.core.validators import MinValueValidator
from rest_framework import serializers


class PriceQueryParamsDeserializer(serializers.Serializer):

    start = serializers.DateTimeField(input_formats=["iso-8601"])
    end = serializers.DateTimeField(input_formats=["iso-8601"])
    days_of_week = serializers.SerializerMethodField()

    # Field level validations

    # Custom logic

    def get_days_of_week(self, obj):
        days = (obj["start"], obj["end"])
        days_list = [
            ParkingRateService().get_shorthand_weekday_name_by_number(iso_format=day)
            for day in days
        ]
        validate_time_range_spans_one_day(days_list)
        return days_list

    # Object level validations

    def validate(self, attrs):
        validate_start_time_is_before_end_time(
            start_time=attrs["start"], end_time=attrs["end"]
        )
        validate_time_range_spans_one_day(self.get_days_of_week(attrs))

        return attrs


# "days": "mon,tues,thurs",
# "times": "0900-2100",
# "tz": "America/Chicago",
# "price": 1500


class RateDeserializer(serializers.Serializer):
    days = serializers.CharField()
    times = serializers.CharField()
    tz = serializers.CharField(label="timezone")
    price = serializers.IntegerField(validators=[MinValueValidator(0)])
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    # Field level validations

    def validate_times(self, value):
        validate_time_range_in_correct_format(times=value)
        return value

    def validate_tz(self, value):
        validate_timezone_name_is_recognized(timezone=value)
        return value

    # Custom logic

    def get_start_time(self, obj):
        """Extract start time and convert to UTC"""
        start_time = obj["times"].split("-", 2)
        return ParkingRateService().convert_plain_text_time_tz_to_utc(
            time=start_time[0], tz=obj["tz"]
        )

    def get_end_time(self, obj):
        """Extract end time and convert to UTC"""
        end_time = obj["times"].split("-", 2)
        return ParkingRateService().convert_plain_text_time_tz_to_utc(
            time=end_time[1], tz=obj["tz"]
        )

    # Object level validations

    def validate(self, data):
        return data