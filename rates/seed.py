import json
from rates.serializers import RateDeserializer


def seed_database_with_parking_rates():
    """Migrates file of given parking rates into database"""
    from rates.models import (
        ParkingRate,
    )  # Needs to stay scoped within this function; otherwise App has not loaded yet

    with open(
        "rates/static_files/sample_rates.json", mode="r", encoding="utf-8"
    ) as sample_rates:
        rates_list = json.loads(sample_rates.read())["rates"]
        deserializer = RateDeserializer(data=rates_list, many=True)
        deserializer.is_valid()
        for item in deserializer.data:
            mapped_item = {
                "days": item["days"],
                "start_time": item["start_time"],
                "end_time": item["end_time"],
                "price": item["price"],
                "original_time_range": item["times"],
                "original_given_timezone": item["tz"],
            }
            ParkingRate.objects.create(**mapped_item)
