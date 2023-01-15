from abc import abstractmethod
from typing import Generic, TypeVar

from models.chat.chat_message import ChatMessage
from utils.abstract_base_classes import Service

Tokens = TypeVar('Tokens')


class IAuthService(Service):

    @abstractmethod
    def authenticate(self, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def try_authenticate(self, token: str) -> bool:
        raise NotImplementedError


class ITokenizerService(Generic[Tokens], Service):

    @abstractmethod
    async def tokenize_async(self, data: str) -> Tokens:
        raise NotImplementedError

    @abstractmethod
    async def decode_async(self, tokens: Tokens) -> str:
        raise NotImplementedError


class IGeneratorService(Generic[Tokens], Service):

    @abstractmethod
    async def generate_async(self, data: Tokens) -> Tokens:
        raise NotImplementedError


class IChatMessageService(Service):

    @abstractmethod
    async def send_async(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def receive_async(self) -> str:
        raise NotImplementedError


class IBotService(Service):

    @abstractmethod
    async def run(self):
        pass


class IChatService(Service):

    @abstractmethod
    async def get_response(self, message: ChatMessage | None) -> str:
        raise NotImplementedError
