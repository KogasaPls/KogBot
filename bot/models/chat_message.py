import dataclasses
from datetime import datetime
from typing import Self

from orjson import orjson
from bot.DAL.entities.chat_message import ChatMessage as ChatMessageEntity
from bot.models.chat_room import ChatRoom
from bot.models.chatter import Chatter
from bot.models.DomainModel import DomainModel


@dataclasses.dataclass
class ChatMessage(DomainModel[ChatMessageEntity]):
    chatter: Chatter
    chat_room: ChatRoom
    message: str
    sent_at_time: datetime

    def bind(self) -> ChatMessageEntity:
        entity = ChatMessageEntity()
        entity.chatter_name = self.chatter.name
        entity.chat_room_name = self.chat_room.name
        entity.message = self.message
        entity.sent_at_time = int(self.sent_at_time.timestamp())
        return entity

    def serialize(self) -> bytes:
        return orjson.dumps(dataclasses.asdict(self)) + b'\n'

    @classmethod
    def deserialize(cls, data: bytes) -> Self | None:
        obj_dict = orjson.loads(data.rstrip(b'\n'))
        msg = ChatMessage(
            chatter=Chatter(name=obj_dict["chatter"]["name"]),
            chat_room=ChatRoom(name=obj_dict["chat_room"]["name"]),
            message=obj_dict["message"],
            sent_at_time=(obj_dict["sent_at_time"]))
        return msg

    def __repr__(self):
        return f"(#{self.chat_room.name}) {self.chatter.name}: {self.message}"
