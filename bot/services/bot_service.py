import asyncio
import sqlite3
import ssl

from faker import Faker
from bot.services.interfaces import IAuthService, IBotService, IChatService
from fake_provider import FakeProvider
from models.chat_message import ChatMessage
from utils.abstract_base_classes import Service


class BotService(IBotService, Service):
    auth_service: IAuthService
    loop: asyncio.AbstractEventLoop

    def __init__(self, config: dict, db: sqlite3.Connection,
                 auth_service: IAuthService, chat_service: IChatService):
        super().__init__(config)
        self.auth_service = auth_service
        self.chat_service = chat_service
        self.ssl_context = self.get_ssl_context()

    async def start(self):
        await self.start_server()

    async def start_server(self):
        await self.logger.info("Starting bot service...")
        server = await asyncio.start_server(self.handle_connection, '127.0.0.1',
                                            8888)

        async with server:
            await self.logger.info(
                f"Now serving on {server.sockets[0].getsockname()}")
            await server.serve_forever()

    async def handle_connection(self, reader, writer, use_tls=False) -> None:
        addr = writer.get_extra_info('peername')
        await self.logger.info(f"Connection established from {addr}")

        if use_tls:
            try:
                # upgrade to TLS
                await self.logger.info(
                    f"Establishing TLS connection with {addr}")
                reader, writer = await writer.start_tls(self.ssl_context)
                await self.logger.info(f"Connection to {addr} upgraded to TLS")
            except Exception as e:
                await self.logger.error(
                    f"Error upgrading connection to TLS: {e}")
                return

        async for data in reader:
            message = data.decode()

            await self.logger.info(f"Received {message!r} from {addr!r}")
            response = await self.get_response(message)

            await self.logger.info(f"Responding to {addr!r}: {response}")
            writer.write(response.encode())
            await writer.drain()

        writer.close()
        await writer.wait_closed()
        await self.logger.info(f"Connection to  {addr!r} closed")

    async def get_response(self, message):
        # TODO: deserialize into ChatMessage here
        fake = Faker()
        fake.add_provider(FakeProvider)
        chat_message: ChatMessage = fake.chat_message()
        chat_message.message = message

        return await self.chat_service.get_response(chat_message) + "\n"

    def get_ssl_context(self):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        return ctx
