from dataclasses import dataclass

from entities.DomainObject import DomainObject


@dataclass
class Chatter:
    id: int
    name: str

    def __repr__(self):
        return self.name


@dataclass
class ChatterDO(DomainObject[Chatter]):
    id: int
    name: str
