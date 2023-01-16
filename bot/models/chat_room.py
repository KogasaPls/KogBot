from entities.chat.chat_room import ChatRoom as ChatRoomEntity

from models.DomainModel import DomainModel


class ChatRoom(DomainModel[ChatRoomEntity]):
    id: int
    name: str

    def __db_mapping__(self):
        yield from {"id": self.id, "name": self.name}
