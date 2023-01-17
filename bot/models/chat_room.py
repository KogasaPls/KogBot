import dataclasses

from bot.DAL.entities.chat_room import ChatRoom as ChatRoomEntity
from bot.models.DomainModel import DomainModel, TEntity


@dataclasses.dataclass
class ChatRoom(DomainModel[ChatRoomEntity]):
    name: str

    def bind(self) -> TEntity:
        entity = ChatRoomEntity()
        entity.name = self.name
        return entity
