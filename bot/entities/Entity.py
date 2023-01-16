import abc
from typing import Self


class Entity(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    def __db_mapping__(self):
        for key in self.__annotations__.keys():
            yield key, getattr(self, key)

    def adapt(self):
        """Converts the entity to a tuple for insertion into the database.
        id is replaced with None to allow the database to generate a new id."""
        return tuple((value if key != "id" else None
                      for key, value in self.__db_mapping__()))

    @classmethod
    def bind(cls, row, t: type) -> Self:
        """Converts a row from the database to an entity."""
        instance = t()
        for key, value in zip(t.__annotations__.keys(), row):
            setattr(instance, key, value)
        return instance
