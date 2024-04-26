from rates.models import ParkingRate
from rates.services.parking_rate_service import ParkingRateService
from rates.utils import get_format_with_datetime
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
        return [
            ParkingRateService().get_shorthand_weekday_name_by_number(iso_format=day)
            for day in days
        ]

    # Object level validations

    def validate(self, attrs):
        validate_start_time_is_before_end_time(
            start_time=attrs["start"], end_time=attrs["end"]
        )
        validate_time_range_spans_one_day(self.get_days_of_week(attrs))

        return attrs


class RateDeserializer(serializers.Serializer):
    days = serializers.CharField()
    times = serializers.CharField()
    tz = serializers.CharField(label="timezone")
    price = serializers.IntegerField(validators=[MinValueValidator(0)])
    start_time_utc = serializers.SerializerMethodField()
    end_time_utc = serializers.SerializerMethodField()
    start_time_original = serializers.SerializerMethodField()
    end_time_original = serializers.SerializerMethodField()

    # Field level validations

    def validate_times(self, value):
        validate_time_range_in_correct_format(times=value)
        return value

    def validate_tz(self, value):
        validate_timezone_name_is_recognized(timezone=value)
        return value

    # Custom logic

    def get_start_time_utc(self, obj):
        """Extract start time and convert to UTC"""
        start_time = ParkingRateService.get_original_time_by_time_range(
            time_range=obj["times"], specific_time="start"
        )
        return ParkingRateService().convert_plain_text_time_tz_to_utc(
            time=start_time, tz=obj["tz"]
        )

    def get_end_time_utc(self, obj):
        """Extract end time and convert to UTC"""
        end_time = ParkingRateService.get_original_time_by_time_range(
            time_range=obj["times"], specific_time="end"
        )
        return ParkingRateService().convert_plain_text_time_tz_to_utc(
            time=end_time, tz=obj["tz"]
        )

    def get_start_time_original(self, obj):
        """Extract original start time in the original timezone"""
        return ParkingRateService.get_original_time_by_time_range(
            obj["times"], specific_time="start"
        )

    def get_end_time_original(self, obj):
        """Extract original end time in the original timezone"""
        return ParkingRateService.get_original_time_by_time_range(
            obj["times"], specific_time="end"
        )

    # Object level validations

    def validate(self, data):
        return data


class RateSerializer(serializers.ModelSerializer):
    times = serializers.CharField(source="original_time_range")
    tz = serializers.CharField(source="original_given_timezone")

    class Meta:
        model = ParkingRate
        fields = ("days", "times", "tz", "price")


class PriceSerializer(RateSerializer):
    class Meta:
        model = ParkingRate
        fields = ("price",)
