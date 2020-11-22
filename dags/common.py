from datetime import datetime

DS_FORMAT = "%Y-%m-%d"


def datetime_to_ds(dt: datetime) -> str:
    return dt.strftime(DS_FORMAT)
