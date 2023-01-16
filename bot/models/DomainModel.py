from abc import ABCMeta
from typing import Generic, TypeVar

from entities.Entity import Entity

TEntity = TypeVar("TEntity", bound=Entity, covariant=True)


class DomainModel(Generic[TEntity], metaclass=ABCMeta):
    pass
