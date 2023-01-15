import sqlite3

from bot.DAL.base_repository import BaseRepository
from entities.chat.chatter import ChatterDO


class ChatterRepository(BaseRepository[ChatterDO]):

    def __init__(self, db: sqlite3.Connection):
        super().__init__(db, "Chatters", 2)

    def adapt(self, chatter: ChatterDO) -> tuple:
        return tuple([chatter.id, chatter.name])

    def convert(self, val: tuple) -> ChatterDO:
        id = val[0]
        name = val[1]
        return ChatterDO(id, name)
