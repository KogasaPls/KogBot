import abc
from typing import Generic, TypeVar

T = TypeVar("T")


class DomainObject(Generic[T], metaclass=abc.ABCMeta):

    def __init__(self, model: T):
        self.copy_attributes(model)

    def copy_attributes(self, model: T):
        for attr in self.__dict__:
            if hasattr(model, attr):
                setattr(self, attr, getattr(model, attr))

    def to_domain_model(self) -> T:
        instance = T()
        for attr in self.__dict__:
            if hasattr(T, attr):
                setattr(instance, attr, getattr(self, attr))
        return instance
