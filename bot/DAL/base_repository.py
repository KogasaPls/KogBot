import sqlite3
from abc import ABCMeta
from typing import Generic, TypeVar

from entities.Entity import Entity

TEntity = TypeVar("TEntity", bound=Entity, covariant=True)


# annotation for repos to assign the number of columns and the table name
def Repo(table_name: str, entity_type: type):
    if not issubclass(entity_type, Entity):
        raise TypeError(f"Type {entity_type} does not extend {Entity}")

    def wrapper(cls):
        cls.type = entity_type
        cls.table_name = table_name
        cls.tuple_format_string = ",".join(
            ["?" for _ in entity_type.__annotations__])
        return cls

    return wrapper


class BaseRepository(Generic[TEntity], metaclass=ABCMeta):
    db: sqlite3.Connection
    table_name: str
    tuple_format_string: str
    type: TEntity

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def commit(self):
        self.db.commit()

    def create(self, obj: TEntity) -> TEntity:
        adapted: tuple = obj.adapt()
        sql = f"""
        INSERT INTO {self.table_name} VALUES ({self.tuple_format_string});
        """
        with self.db as db:
            db.execute(sql, adapted)
            id = db.execute("SELECT last_insert_rowid();").fetchone()[0]
            obj.id = id
            return obj

    def create_many(self, objs: list[TEntity]):
        adapted = [obj.adapt() for obj in objs]
        sql = f"""
        INSERT INTO {self.table_name} VALUES ({self.tuple_format_string});
        """
        with self.db as db:
            db.executemany(sql, adapted)

    def get_all(self) -> list[TEntity]:
        sql = f"""
        SELECT * FROM {self.table_name};
        """
        with self.db as db:
            return db.execute(sql).fetchall()

    def find(self, **kwargs) -> list[TEntity]:
        sql = f"""
        SELECT * FROM {self.table_name} WHERE
        """
        sql += " AND ".join([f"{k} = ?" for k in kwargs.keys()])
        rows = self.db.execute(sql, tuple(kwargs.values())).fetchall()
        return [Entity.bind(row, self.type) for row in rows]
