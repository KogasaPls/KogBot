from datetime import datetime

from entities.chat.chat_message import ChatMessage as ChatMessageEntity

from models.chat_room import ChatRoom
from models.chatter import Chatter
from models.DomainModel import DomainModel


class ChatMessage(DomainModel[ChatMessageEntity]):

    def __db_attrs__(self) -> dict:
        pass

    chatter: Chatter
    chat_room: ChatRoom
    message: str
    sent_at_time: datetime = datetime.now()
    id: int = None

    def __db_mapping__(self):
        yield from {
            "id": self.id,
            "chatter_id": self.chatter.id,
            "chat_room_id": self.chat_room.id,
            "message": self.message,
            "sent_at_time": self.sent_at_time,
        }
