import sqlite3

from bot.DAL.base_repository import BaseRepository, Repo
from bot.entities.chat.chat_message import ChatMessage


@Repo("ChatMessages", ChatMessage)
class ChatMessageRepository(BaseRepository[ChatMessage]):

    def __init__(self, db: sqlite3.Connection):
        super().__init__(db)
