from datetime import datetime
from typing import Self

from entities.chat.chat_message import ChatMessage as ChatMessageEntity

from models.chat_room import ChatRoom
from models.chatter import Chatter
from models.DomainModel import DomainModel, TEntity


class ChatMessage(DomainModel[ChatMessageEntity]):
    chatter: Chatter
    chat_room: ChatRoom
    message: str
    sent_at_time: datetime = datetime.now()
    id: int = None

    def bind(self) -> TEntity:
        pass

    @classmethod
    def convert(cls, entity: TEntity) -> Self:
        pass

    def __db_attrs__(self) -> dict:
        pass
