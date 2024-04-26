import pytest
from rates.models import ParkingRate


@pytest.fixture
def parking_rate_mon_tues_thurs():
    data = {
        "days": "mon,tues,thurs",
        "start_time_utc": "14:00:00",
        "end_time_utc": "02:00:00",
        "start_time_original": "09:00:00",
        "end_time_original": "21:00:00",
        "original_time_range": "0900-2100",
        "original_given_timezone": "America/Chicago",
        "price": 1500,
    }
    return ParkingRate.objects.create(**data)


@pytest.fixture
def parking_rate_wed():
    data = {
        "days": "wed",
        "start_time_utc": "11:00:00",
        "end_time_utc": "23:00:00",
        "start_time_original": "06:00:00",
        "end_time_original": "18:00:00",
        "original_time_range": "0600-1800",
        "original_given_timezone": "America/Chicago",
        "price": 1750,
    }
    return ParkingRate.objects.create(**data)


@pytest.fixture
def parking_rate_mon_wed_sat():
    data = {
        "days": "mon,wed,sat",
        "start_time_utc": "06:00:00",
        "end_time_utc": "10:00:00",
        "start_time_original": "01:00:00",
        "end_time_original": "05:00:00",
        "original_time_range": "0100-0500",
        "original_given_timezone": "America/Chicago",
        "price": 1000,
    }
    return ParkingRate.objects.create(**data)


@pytest.fixture
def parking_rate_fri_sat_sun():
    data = {
        "days": "fri,sat,sun",
        "start_time_utc": "14:00:00",
        "end_time_utc": "02:00:00",
        "start_time_original": "09:00:00",
        "end_time_original": "21:00:00",
        "original_time_range": "0900-2100",
        "original_given_timezone": "America/Chicago",
        "price": 2000,
    }
    return ParkingRate.objects.create(**data)


@pytest.fixture
def all_parking_rates(
    parking_rate_mon_tues_thurs,
    parking_rate_wed,
    parking_rate_mon_wed_sat,
    parking_rate_fri_sat_sun,
):
    return {
        parking_rate_mon_tues_thurs,
        parking_rate_wed,
        parking_rate_mon_wed_sat,
        parking_rate_fri_sat_sun,
    }
