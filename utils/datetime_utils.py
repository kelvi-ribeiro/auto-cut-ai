def get_datetime_without_milliseconds(datetime):
    return datetime.isoformat(sep=" ", timespec="seconds")