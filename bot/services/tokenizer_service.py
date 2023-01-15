import asyncio
from dataclasses import dataclass

from transformers import AutoTokenizer, GPT2Tokenizer
from bot.services.interfaces import ITokenizerService, Tokens


@dataclass
class TokenizerService(ITokenizerService):
    tokenizer_name: str
    tokenizer: GPT2Tokenizer

    def __init__(self, config: dict, *args, **kwargs):
        super().__init__(config)
        self.tokenizer_name = config["tokenizer"]["name"]

    async def __init_async__(self):
        await super().__init_async__()
        await self.load_tokenizer()

    async def load_tokenizer(self) -> None:
        await self.logger.debug(
            f"Loading tokenizer \"{self.tokenizer_name}\"...")
        self.tokenizer = await asyncio.get_running_loop().run_in_executor(
            None, AutoTokenizer.from_pretrained, self.tokenizer_name)
        await self.logger.debug("Tokenizer loaded.")

    def tokenize(self, data: str) -> Tokens:
        tokens = self.tokenizer.encode(data, return_tensors="pt")
        return tokens

    async def tokenize_async(self, data: str) -> Tokens:
        self.logger.debug(f"Tokenizing \"{data}\"...")
        tokens = await asyncio.get_running_loop().run_in_executor(
            None, self.tokenize, data)
        self.logger.debug(f"Tokenized \"{data}\" to {tokens}")

        return tokens

    def decode(self, tokens: Tokens) -> str:
        return self.tokenizer.decode(tokens)

    async def decode_async(self, tokens: Tokens) -> str:
        return await asyncio.get_running_loop().run_in_executor(
            None, self.decode, tokens)
