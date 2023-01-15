import sqlite3

from bot.services.interfaces import IAuthService


class AuthService(IAuthService):
    db: sqlite3.Connection

    def __init__(self, config: dict, db: sqlite3.Connection):
        super().__init__(config)
        self.db = db

    def authenticate(self, token: str) -> None:
        pass

    def try_authenticate(self, token: str) -> bool:
        pass

    def dispose(self):
        pass
