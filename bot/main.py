import asyncio

from entities.chat.chat_message import ChatMessage
from entities.chat.chatter import Chatter
from services.interfaces import IChatService
from utils.dependency_injection import Container


async def main(container: Container):
    logger = container.logger()
    await logger.info("Starting...")

    chat_service: IChatService = await container.chat_service()

    chatter: Chatter = Chatter("Test Chatter")
    message = ChatMessage(chatter, "Hello, world!")
    out = await chat_service.get_response(message)
    await logger.info(out)


if __name__ == "__main__":
    asyncio.run(main(Container()))
