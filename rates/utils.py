from datetime import datetime


def get_format_with_datetime(iso_datetime: str) -> datetime:
    """Create a datetime object from an ISO-8601 formatted string"""
    iso_format = replace_space_w_plus(iso_datetime)
    return datetime.fromisoformat(iso_format)


def replace_space_w_plus(string_dt: str) -> str:
    """
    The '+' in the ISO-8601 formatted times were not being encoded - they were
    being ingested as a space so this is a hacky way to get around the format errors
    """
    if any(c.isspace() for c in string_dt):
        return string_dt.replace(" ", "+")
    return string_dt
