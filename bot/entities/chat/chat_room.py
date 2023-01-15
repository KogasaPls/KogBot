from dataclasses import dataclass

from entities.DomainObject import DomainObject


@dataclass
class ChatRoom:
    id: int
    name: str


@dataclass
class ChatRoomDO(DomainObject[ChatRoom]):
    id: int
    name: str
