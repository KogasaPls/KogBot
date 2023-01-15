import sqlite3

from bot.DAL.base_repository import BaseRepository
from entities.chat.chatter import Chatter


class ChatterRepository(BaseRepository[Chatter]):

    def __init__(self, db: sqlite3.Connection):
        super().__init__(db, "Chatters", 2)

    def adapt(self, chatter: Chatter) -> tuple:
        return tuple([chatter.id, chatter.name])

    def convert(self, val: tuple) -> Chatter:
        id = val[0]
        name = val[1]
        return Chatter(id, name)

    def get_chatter_by_name(self, name: str) -> Chatter:
        sql = """SELECT * FROM Chatters WHERE name = ?"""
        row = self.db.execute(sql, (name,)).fetchone()
        return self.convert(row)
