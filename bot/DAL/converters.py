import sqlite3
from datetime import datetime


def adapt_datetime_epoch(val: datetime) -> int:
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())


def convert_timestamp(val: str) -> datetime:
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.fromtimestamp(int(val))


sqlite3.register_adapter(datetime, adapt_datetime_epoch)
sqlite3.register_converter("sent_at_time", convert_timestamp)
