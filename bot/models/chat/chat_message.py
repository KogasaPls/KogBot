import datetime
from dataclasses import dataclass

from bot.models.chat.chatter import Chatter


@dataclass
class ChatMessage:
    sender: Chatter
    text: str
    timestamp: datetime.datetime = datetime.datetime.now()

    def __repr__(self):
        return f"{self.sender}: \"{self.text}\""
