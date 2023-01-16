from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from entities.Entity import Entity

T = TypeVar("T", bound=Entity, covariant=True)


class DomainModel(Generic[T], metaclass=ABCMeta):

    @abstractmethod
    def __db_attrs__(self) -> dict:
        pass

    def adapt(self) -> tuple:
        attrs = self.__db_attrs__()
        return tuple([attrs[key] for key in attrs])

    @classmethod
    def convert(cls, row: tuple) -> T:
        pass
