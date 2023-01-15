import sqlite3
from datetime import datetime

from entities.chat.chat_message import ChatMessage


def adapt_datetime_epoch(val: datetime) -> int:
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())


def convert_timestamp(val: str) -> datetime:
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.fromtimestamp(int(val))


def convert_chat_message(val: str) -> ChatMessage:
    """Convert string to ChatMessage object."""
    return ChatMessage(*val.split(" "))


sqlite3.register_adapter(datetime, adapt_datetime_epoch)
sqlite3.register_converter("timestamp", convert_timestamp)
