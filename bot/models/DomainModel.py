from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from entities.Entity import Entity

TEntity = TypeVar("TEntity", bound=Entity, covariant=True)


class DomainModel(Generic[TEntity], metaclass=ABCMeta):
    pass

    def adapt(self) -> tuple:
        """Forwards to the underlying entity's adapt method."""
        entity = self.bind()
        return entity.adapt()

    @abstractmethod
    def bind(self) -> TEntity:
        """Binds a domain model to an entity."""
        pass
