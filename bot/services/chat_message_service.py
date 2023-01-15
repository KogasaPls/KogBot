import sqlite3

from bot.services.interfaces import IChatMessageService


class ChatMessageService(IChatMessageService):
    db: sqlite3.Connection

    def __init__(self, config: dict, db: sqlite3.Connection):
        super().__init__(config)
        self.db = db

    async def send_async(self, message: str) -> None:
        pass

    async def receive_async(self) -> str:
        pass

    def dispose(self):
        pass
