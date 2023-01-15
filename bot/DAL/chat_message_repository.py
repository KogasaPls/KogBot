import sqlite3

from bot.DAL.base_repository import BaseRepository
from bot.entities.chat.chat_message import ChatMessageDO


class ChatMessageRepository(BaseRepository[ChatMessageDO]):

    def __init__(self, db: sqlite3.Connection):
        super().__init__(db, "ChatMessages", 5)

    def adapt(self, message: ChatMessageDO) -> tuple:
        return tuple([
            message.id, message.chatter_id, message.chat_room_id,
            message.message, message.sent_at_time
        ])

    def convert(self, val: tuple) -> ChatMessageDO:
        id = val[0]
        chatter_id = val[1]
        chat_room_id = val[2]
        message = val[3]
        sent_at_time = val[4]
        return ChatMessageDO(id, chatter_id, chat_room_id, message,
                             sent_at_time)
