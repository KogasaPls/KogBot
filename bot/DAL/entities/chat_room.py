import dataclasses

from bot.DAL.entity import Entity


@dataclasses.dataclass
class ChatRoom(Entity):
    id: int
    name: str

    def __init__(self):
        super().__init__()
