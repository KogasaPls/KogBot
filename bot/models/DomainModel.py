from abc import ABCMeta
from typing import Generic, TypeVar

from entities.Entity import Entity

T = TypeVar("T", bound=Entity, covariant=True)


class DomainModel(Generic[T], metaclass=ABCMeta):
    pass
