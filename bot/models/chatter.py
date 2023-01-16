from bot.entities.chat.chatter import Chatter as ChatterEntity

from models.DomainModel import DomainModel


class Chatter(DomainModel[ChatterEntity]):
    id: int
    name: str

    def __db_mapping__(self):
        yield from {
            "id": self.id,
            "name": self.name,
        }

    def __repr__(self):
        return self.name
