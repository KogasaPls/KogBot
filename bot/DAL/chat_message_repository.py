import sqlite3

from bot.DAL.base_repository import BaseRepository
from bot.entities.chat.chat_message import ChatMessage


class ChatMessageRepository(BaseRepository[ChatMessage]):

    def __init__(self, db: sqlite3.Connection):
        super().__init__(db, "ChatMessages", 4)

    def create_chat_messaeg(self, message: ChatMessage) -> None:
        sql = f"""
            INSERT INTO ChatMessages
                (
                    ChatterId,
                    ChatRoomId,
                    Message,
                    SentAtTime
                )
            VALUES
                (
                    (SELECT Id FROM Chatters WHERE Name = @chatterName),
                    (SELECT Id FROM ChatRooms WHERE Name = @chatRoomName),
                    @Message,
                    @SentAtTime
                )
                """
        cmd = self.db.executescript()
