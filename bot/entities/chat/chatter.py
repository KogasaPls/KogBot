from dataclasses import dataclass


@dataclass
class Chatter:
    id: int
    name: str

    def __repr__(self):
        return self.name
