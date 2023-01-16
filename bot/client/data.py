import dataclasses
import pickle
from typing import TypeVar

T = TypeVar("T")


@dataclasses.dataclass
class DataPackage:
    message: str
    user: str
    channel: str
    time: str

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data: bytes) -> "DataPackage":
        return pickle.loads(data)
