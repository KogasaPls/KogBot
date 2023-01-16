import dataclasses

from entities.Entity import Entity


@dataclasses.dataclass
class ChatMessage(Entity):
    id: int
    chatter_id: int
    chat_room_id: int
    message: str
    sent_at_time: int

    def __init__(self):
        super().__init__()
