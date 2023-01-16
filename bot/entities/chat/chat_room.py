import dataclasses

from entities.Entity import Entity


@dataclasses.dataclass
class ChatRoom(Entity):
    id: int
    name: str
