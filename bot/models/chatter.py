import dataclasses

from bot.DAL.entities.chatter import Chatter as ChatterEntity
from bot.models.DomainModel import DomainModel, TEntity


@dataclasses.dataclass
class Chatter(DomainModel[ChatterEntity]):
    name: str

    def __db_mapping__(self):
        yield from {
            "name": self.name,
        }

    def __repr__(self):
        return self.name

    def bind(self) -> TEntity:
        entity = ChatterEntity()
        entity.name = self.name
        return entity
