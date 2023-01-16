import asyncio

from utils.dependency_injection import Container


async def main(container: Container):
    logger = container.logger()
    await logger.info("Starting...")
    bot_service = await container.bot_service()
    await bot_service.start()


if __name__ == "__main__":
    asyncio.run(main(Container()))
