import asyncio
import sqlite3
import ssl
from asyncio import Server

from bot.models.chat_message import ChatMessage
from bot.services.chat_service import ChatService
from bot.services.interfaces import IAuthService, IBotService
from utils.abstract_base_classes import Service


class BotService(IBotService, Service):
    auth_service: IAuthService
    loop: asyncio.AbstractEventLoop

    def __init__(self, config: dict, db: sqlite3.Connection,
                 auth_service: IAuthService, chat_service: ChatService):
        super().__init__(config)
        self.auth_service = auth_service
        self.chat_service = chat_service
        self.ssl_context = self.get_ssl_context()

    async def start(self):
        await self.start_server()

    async def start_server(self):
        await self.logger.info("Starting bot service...")
        server: Server = await asyncio.start_server(self.handle_connection,
                                                    '127.0.0.1', 8888)

        async with server:
            await self.logger.info(
                f"Now serving on {server.sockets[0].getsockname()}")
            await server.serve_forever()

    async def handle_connection(self, reader, writer, use_tls=False) -> None:
        addr = writer.get_extra_info('peername')
        await self.logger.info(f"Connection established from {addr}")

        if use_tls:
            reader, writer = await self.upgrade_connection(addr, writer)

        while await self.do_connection_loop(addr, reader, writer):
            pass

        await self.close_connection(addr, writer)

    async def upgrade_connection(self, addr, writer):
        # upgrade to TLS
        await self.logger.info(f"Establishing TLS connection with {addr}")
        reader, writer = await writer.start_tls(self.ssl_context)
        await self.logger.info(f"Connection to {addr} upgraded to TLS")
        return reader, writer

    async def do_connection_loop(self, addr, reader, writer):
        try:
            data = await reader.readline()
            message = ChatMessage.deserialize(data)
        except Exception as e:
            await self.logger.error(f"{addr} - Could not deserialize data, {e}")
            return False

        await self.logger.info(f"{addr.__repr__()} RECV: {message.__repr__()}")

        try:
            response = await self.get_response_or_none(message)
            if not response:
                return True

            await self.logger.info(
                f"{addr.__repr__()} SEND: {response.__repr__()}")
            writer.write(response.encode())
            await writer.drain()
        except Exception as e:
            await self.logger.error(
                f"{addr.__repr__()} - Error getting response: {e}")
            await self.logger.debug(
                f"{addr.__repr__()} - In reply to: {message.__repr__()}")
            return False

        return True

    async def close_connection(self, addr, writer):
        await self.logger.info(f"Closing connection to {addr}")
        writer.close()
        await writer.wait_closed()
        await self.logger.info(f"Connection to {addr} closed")

    async def get_response_or_none(self, message):
        response = await self.chat_service.get_response(message)
        return response + "\n" if response else None

    def get_ssl_context(self):
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        return ctx
