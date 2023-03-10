import sqlite3

from bot.DAL.base_repository import BaseRepository, Repo
from bot.DAL.entities.chatter import Chatter


@Repo("Chatters", Chatter)
class ChatterRepository(BaseRepository[Chatter]):

    def __init__(self, db: sqlite3.Connection):
        super().__init__(db)
