import asyncio
import sqlite3

import torch
from torch import Tensor
from transformers import AutoModelForCausalLM, GPT2LMHeadModel
from bot.services.interfaces import IGeneratorService


class ModelConfig:

    def __init__(self, config: dict):
        self.name = config["name"]
        self.device = config["device"]
        self.do_sample = bool(config["do_sample"])
        self.num_return_sequences = int(config["num_return_sequences"])
        self.max_new_tokens = int(config["max_new_tokens"])
        self.min_length = int(config["min_length"])
        self.top_k = int(config["top_k"])
        self.top_p = float(config["top_p"])
        self.temperature = float(config["temperature"])
        self.repetition_penalty = float(config["repetition_penalty"])
        self.length_penalty = float(config["length_penalty"])
        self.no_repeat_ngram_size = int(config["no_repeat_ngram_size"])


class GeneratorService(IGeneratorService[Tensor]):
    db: sqlite3.Connection
    model_config: ModelConfig
    model: GPT2LMHeadModel

    def __init__(self, config: dict, db: sqlite3.Connection):
        super().__init__(config)
        self.db = db
        self.config = config["generator_service"]
        self.model_config = ModelConfig(config["model"])

    async def __init_async__(self):
        await self.load_model()

    def generate(self, data: Tensor) -> Tensor:
        return asyncio.run(self.generate_async(data))

    async def load_model(self):
        await self.logger.debug(f"Loading model \"{self.model_config.name}\"..."
                               )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_config.name).to(self.model_config.device)
        await self.logger.debug("Model loaded.")

    async def generate_async(self,
                             input_tokens: Tensor | list[Tensor],
                             eos_token: Tensor | None = None) -> Tensor:
        if isinstance(input_tokens, list):
            input_tokens = torch.cat(input_tokens, dim=1)
        num_input_tokens = input_tokens.shape[1]

        input_tokens = input_tokens.to(self.model_config.device)
        attention_mask: Tensor = torch.ones_like(input_tokens).to(
            self.model_config.device)

        await self.logger.debug(
            f"Generating output for {num_input_tokens} input tokens...")
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(
            None, lambda: self.model.generate(
                input_tokens,
                attention_mask=attention_mask,
                eos_token_id=int(eos_token[0][0]
                                ) or self.model.config.eos_token_id,
                max_new_tokens=self.model_config.max_new_tokens,
                no_repeat_ngram_size=self.model_config.no_repeat_ngram_size,
                min_length=self.model_config.min_length,
                do_sample=self.model_config.do_sample,
                top_k=self.model_config.top_k,
                top_p=self.model_config.top_p,
                num_return_sequences=self.model_config.num_return_sequences,
                temperature=self.model_config.temperature,
                repetition_penalty=self.model_config.repetition_penalty,
                length_penalty=self.model_config.length_penalty)[0])

        trimmed_output = output[num_input_tokens:]
        await self.logger.debug(f"Generated {trimmed_output.shape[0]} tokens.")
        return trimmed_output
