from datetime import datetime


def get_format_with_datetime(iso_datetime: str):
    return datetime.fromisoformat(iso_datetime)
