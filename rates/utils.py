from datetime import datetime


def get_format_with_datetime(iso_datetime: str):
    iso_datetime = iso_datetime.replace(" ", "+")
    return datetime.fromisoformat(iso_datetime)


def replace_space_w_plus(string_dt: str) -> str:
    if any(c.isspace() for c in string_dt):
        return string_dt.replace(" ", "+")
    return string_dt
