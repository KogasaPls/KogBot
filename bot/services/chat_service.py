import asyncio
import collections
import dataclasses
import sqlite3
from typing import Generic

from bot.services.interfaces import (IGeneratorService, ITokenizerService,
                                     Tokens)
from models.chat.chat_message import ChatMessage
from utils.abstract_base_classes import Service


def initial_deque_factory(cls):
    return collections.deque(maxlen=cls.max_messages)


@dataclasses.dataclass
class TokenizedChatMessage(Generic[Tokens]):
    message: ChatMessage
    tokens: Tokens


class ChatContext(Generic[Tokens]):
    max_messages: int
    messages: collections.deque[TokenizedChatMessage[Tokens]]
    lock: asyncio.Lock = asyncio.Lock()

    def __init__(self, max_messages: int):
        self.max_messages: int = max_messages
        self.messages = collections.deque(maxlen=max_messages)

    async def add_message_with_tokens(self, message: ChatMessage,
                                      tokens: Tokens) -> None:
        tokenized_message = TokenizedChatMessage(message, tokens)
        async with self.lock:
            self.messages.append(tokenized_message)

    async def get_messages(self) -> list[ChatMessage]:
        async with self.lock:
            return list(map(lambda m: m.message, self.messages))

    async def get_tokens(self) -> list[Tokens]:
        async with self.lock:
            tokens = list(map(lambda m: m.tokens, self.messages))
        return tokens


class ChatServiceConfig:
    max_messages: int
    prompt_duplication_factor: int

    def __init__(self, config: dict):
        self.max_messages = int(config["max_messages"])
        self.prompt_duplication_factor = int(
            config["prompt_duplication_factor"])


class ChatService(Service, Generic[Tokens]):
    generator_service: IGeneratorService[Tokens]
    tokenizer_service: ITokenizerService[Tokens]

    lock: asyncio.Lock = asyncio.Lock()

    context: ChatContext[Tokens]

    def __init__(self, config: dict, db: sqlite3.Connection,
                 tokenizer_service: ITokenizerService[Tokens],
                 generator_service: IGeneratorService[Tokens]):
        super().__init__(config)
        self.config = ChatServiceConfig(config["chat_service"])
        self.db = db
        self.tokenizer_service = tokenizer_service
        self.generator_service = generator_service
        self.context = ChatContext[Tokens](
            max_messages=int(self.config.max_messages))

    async def get_response(self, prompt: ChatMessage | None) -> str:
        self.logger.info(f"Getting response to {prompt}")
        tokens = await self.context.get_tokens()
        if prompt is not None:
            prompt_tokens = await self.tokenize(prompt)
            for _ in range(0, self.config.prompt_duplication_factor):
                tokens.append(prompt_tokens)
        model_output = await self.generator_service.generate_async(tokens)

        response = await self.decode(model_output)
        self.logger.debug(f"Generated response: {response}")
        return response

    async def decode(self, tokens: Tokens) -> str:
        decoded = await self.tokenizer_service.decode_async(tokens)
        return decoded

    async def tokenize(self, message: ChatMessage):
        return await self.tokenizer_service.tokenize_async(message.text)
