import asyncio
import collections
import dataclasses
import sqlite3
from typing import Generic

from regex import regex
from bot.models.chat_message import ChatMessage
from bot.services.interfaces import (IChatService, IGeneratorService,
                                     ITokenizerService, Tokens)
from utils.abstract_base_classes import Service


def initial_deque_factory(cls):
    return collections.deque(maxlen=cls.max_messages)


@dataclasses.dataclass
class TokenizedChatMessage(Generic[Tokens]):
    message: ChatMessage
    tokens: Tokens
    num_tokens: int


class ChatContext(Generic[Tokens]):
    tokens: collections.deque[Tokens]
    lock: asyncio.Lock = asyncio.Lock()

    def __init__(self, max_tokens: int):
        self.messages = collections.deque(maxlen=max_tokens)

    async def add_tokens(self, list_of_tokens: list[Tokens]) -> None:
        async with self.lock:
            self.messages.extend(list_of_tokens)

    async def get_tokens(self) -> list[Tokens]:
        async with self.lock:
            return list(self.messages)


class ChatServiceConfig:
    max_messages: int
    prompt_duplication_factor: int

    def __init__(self, config: dict):
        self.max_messages = int(config["max_messages"])
        self.prompt_duplication_factor = int(
            config["prompt_duplication_factor"])
        self.trigger_word = config["trigger_word"]


class ChatService(IChatService, Service, Generic[Tokens]):
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
        self.context = ChatContext[Tokens](int(self.config.max_messages))
        self.newline_token = self.tokenizer_service.get_newline_token()
        self.trigger_pattern = regex.compile(self.config.trigger_word)

    async def get_response(self, prompt: ChatMessage | None) -> str | None:
        await self.handle_incoming_message(prompt)
        if self.is_trigger(prompt):
            return await self.handle_reply(prompt)

    async def handle_reply(self, prompt: ChatMessage) -> str:
        tokens = await self.get_context_tokens()

        if prompt is None:
            await self.logger.info("Getting chat message with no prompt.")
        else:
            await self.logger.info(f"Getting response to {prompt.__repr__()}")
            tokens = await self.prime_tokens_for_prompt(tokens, prompt)

        response = await self.get_model_output(tokens)
        return response

    async def get_context_tokens(self) -> list[Tokens]:
        tokens = await self.context.get_tokens()
        if tokens:
            await self.logger.debug(f"Context tokens: {tokens.__repr__()}")
        return tokens

    async def handle_incoming_message(self, message: ChatMessage | None):
        if message is None:
            return

        tokens = await self.tokenize(message)
        await self.context.add_tokens(tokens)

    def is_trigger(self, message: ChatMessage | None) -> bool:
        return self.trigger_pattern.match(message.message) is not None

    async def prime_tokens_for_prompt(self, tokens: Tokens,
                                      prompt: ChatMessage):
        prompt_tokens = await self.tokenize(prompt)
        for _ in range(0, self.config.prompt_duplication_factor):
            tokens.extend(prompt_tokens)
        return tokens

    async def get_model_output(self, tokens: Tokens) -> str:
        model_output = await self.generator_service.generate_async(
            tokens, self.newline_token)
        response = await self.decode(model_output)
        if response.count("\n") > 0:
            await self.logger.warning("Response contains newline(s).")

        await self.logger.debug("Model output: " + str(model_output))
        return response

    async def decode(self, tokens: Tokens) -> str:
        return await self.tokenizer_service.decode_async(tokens)

    async def tokenize(self, message: ChatMessage) -> Tokens:
        return await self.tokenizer_service.tokenize_async(message.message +
                                                           "\n")
