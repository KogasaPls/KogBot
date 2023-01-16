from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

from entities.Entity import Entity

TEntity = TypeVar("TEntity", bound=Entity, covariant=True)


class DomainModel(Generic[TEntity], metaclass=ABCMeta):
    pass

    @classmethod
    @abstractmethod
    def convert(cls, entity: TEntity) -> Self:
        """Converts an entity to a domain model."""
        pass

    @abstractmethod
    def bind(self) -> TEntity:
        """Binds a domain model to an entity."""
        pass
