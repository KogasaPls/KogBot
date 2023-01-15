import abc
import datetime
import sqlite3
from dataclasses import dataclass
from typing import Generic, TypeVar

from bot.entities.chat.chatter import Chatter
from entities.chat.chat_room import ChatRoom

T = TypeVar("T")


class DomainObject(Generic[T], metaclass=abc.ABCMeta):

    def __init__(self, model: T):
        self.copy_attributes(model)

    def copy_attributes(self, model: T):
        for attr in self.__dict__:
            if hasattr(model, attr):
                setattr(self, attr, getattr(model, attr))

    def to_domain_model(self) -> T:
        instance = T()
        for attr in self.__dict__:
            if hasattr(T, attr):
                setattr(instance, attr, getattr(self, attr))
        return instance


@dataclass
class ChatMessage:
    chatter: Chatter
    chat_room: ChatRoom
    message: str
    sent_at_time: datetime.datetime = datetime.datetime.now()
    id: int = None

    def __repr__(self):
        return f"{self.chatter}: \"{self.message}\""

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.chatter.name} {self.chat_room.name} {self.message} {self.sent_at_time}"


@dataclass
class ChatMessageDO(DomainObject[ChatMessage]):
    id: int
    chatter_id: int
    chat_room_id: int
    message: str
    sent_at_time: int

    @classmethod
    def from_chat_message(cls, message: ChatMessage):
        return cls(message.id, message.chatter.id, message.chat_room.id,
                   message.message, int(message.sent_at_time.timestamp()))
