import json
from rates.serializers import RateDeserializer


def seed_database_with_parking_rates():
    """Migrates file of given parking rates into database"""
    from rates.models import (
        ParkingRate,
    )  # Needs to stay scoped within this function; otherwise App has not loaded yet

    if ParkingRate.objects.all().count() > 1:
        # Return if there are already rows populated to prevent duplicates
        print("ParkingRate objects already populated \nReturning...")
        return

    with open(
        "rates/static_files/sample_rates.json", mode="r", encoding="utf-8"
    ) as sample_rates:
        rates_list = json.loads(sample_rates.read())["rates"]
        deserializer = RateDeserializer(data=rates_list, many=True)
        deserializer.is_valid()
        for item in deserializer.data:
            mapped_item = {
                "days": item["days"],
                "start_time_utc": item["start_time_utc"],
                "end_time_utc": item["end_time_utc"],
                "start_time_original": item["start_time_original"],
                "end_time_original": item["end_time_original"],
                "price": item["price"],
                "original_time_range": item["times"],
                "original_given_timezone": item["tz"],
            }
            ParkingRate.objects.create(**mapped_item)
