import asyncio
from abc import ABCMeta

from utils.log import log


@log
class Service(metaclass=ABCMeta):
    """An abstract base class for services."""

    lock: asyncio.Lock = asyncio.Lock()

    def __init__(self, config: dict):
        self.config = config
        self.logger = self.logger_factory(config)

    async def __init_async__(self):
        await self.logger.debug(f"__init_async__")

    async def __callback__(self):
        await self.logger.debug(f"__callback__")

    def dispose(self):
        pass
