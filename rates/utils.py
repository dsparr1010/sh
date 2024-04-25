from datetime import datetime


def get_format_with_datetime(iso_datetime: str):
    iso_datetime = iso_datetime.replace(" ", "+")
    return datetime.fromisoformat(iso_datetime)
