import sqlite3
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

Entity = TypeVar('Entity')


class BaseRepository(Generic[Entity], metaclass=ABCMeta):
    db: sqlite3.Connection
    table_name: str
    tuple_format_string: str

    def __init__(self, db: sqlite3.Connection, table_name: str,
                 num_params: int):
        self.db = db
        self.table_name = table_name
        self.tuple_format_string = ",".join(["?"] * num_params)

    @abstractmethod
    def adapt(self, obj: Entity) -> tuple:
        pass

    @abstractmethod
    def convert(self, val: str) -> Entity:
        pass

    def commit(self):
        self.db.commit()

    def create(self, obj: Entity):
        adapted: tuple = self.adapt(obj)
        sql = f"""
        INSERT INTO {self.table_name} VALUES ({self.tuple_format_string});
        """
        with self.db as db:
            db.execute(sql, adapted)

    def create_many(self, objs: list[Entity]):
        adapted = [self.adapt(obj) for obj in objs]
        sql = f"""
        INSERT INTO {self.table_name} VALUES ({self.tuple_format_string});
        """
        with self.db as db:
            db.executemany(sql, adapted)

    def get_all(self) -> list[Entity]:
        sql = f"""
        SELECT * FROM {self.table_name};
        """
        with self.db as db:
            return db.execute(sql).fetchall()
