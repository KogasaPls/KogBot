from entities.chat.chat_room import ChatRoom as ChatRoomEntity

from models.DomainModel import DomainModel, TEntity


class ChatRoom(DomainModel[ChatRoomEntity]):
    id: int
    name: str

    def __db_mapping__(self):
        yield from {"id": self.id, "name": self.name}

    def bind(self) -> TEntity:
        entity = ChatRoomEntity()
        entity.id = self.id
        entity.name = self.name
        return entity
