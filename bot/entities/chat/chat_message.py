import dataclasses

from entities.Entity import Entity


@dataclasses.dataclass
class ChatMessage(Entity):
    chatter_id: int
    chat_room_id: int
    message: str
    sent_at_time: int
    id: int = None
