from dataclasses import dataclass


@dataclass
class Chatter:
    name: str

    def __repr__(self):
        return self.name
