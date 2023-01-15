import datetime
import sqlite3
from dataclasses import dataclass

from bot.entities.chat.chatter import Chatter
from entities.chat.chat_room import ChatRoom


@dataclass
class ChatMessage:
    sender: Chatter
    chat_room: ChatRoom
    message: str
    sent_at_time: datetime.datetime = datetime.datetime.now()

    def __repr__(self):
        return f"{self.sender}: \"{self.message}\""

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.sender.name} {self.chat_room.name} {self.message} {self.sent_at_time}"
