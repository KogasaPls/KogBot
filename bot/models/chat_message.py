from datetime import datetime

from entities.chat.chat_message import ChatMessage as ChatMessageEntity

from models.chat_room import ChatRoom
from models.chatter import Chatter
from models.DomainModel import DomainModel


class ChatMessage(DomainModel[ChatMessageEntity]):
    chatter: Chatter
    chat_room: ChatRoom
    message: str
    sent_at_time: datetime = datetime.now()
    id: int = None

    def bind(self) -> ChatMessageEntity:
        entity = ChatMessageEntity()
        entity.id = self.id
        entity.chatter_name = self.chatter.name
        entity.chat_room_name = self.chat_room.name
        entity.message = self.message
        entity.sent_at_time = self.sent_at_time
        entity.chatter_id = self.chatter.id
        entity.chat_room_id = self.chat_room.id
        return entity

    def __db_attrs__(self) -> dict:
        pass
