import asyncio
import dataclasses
import pickle
import ssl

from dotenv import dotenv_values
from twitchio.ext import commands


@dataclasses.dataclass
class DataPackage:
    message: str
    user: str
    channel: str
    time: str

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data: bytes) -> "DataPackage":
        return pickle.loads(data)


def adapt(message):
    return DataPackage(message.content, message.author.name,
                       message.channel.name, message.timestamp)


class TwitchBot(commands.Bot):

    def __init__(self):
        config = dotenv_values(".env")
        super().__init__(token=config["TWITCH_TOKEN"],
                         prefix='?',
                         initial_channels=[config["TWITCH_CHANNEL"]])
        self.ssl_context = self.get_ssl_context()
        self.stream_reader, self.stream_writer = None, None

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        self.stream_reader, self.stream_writer = await asyncio.open_connection(
            '127.0.0.1', 8888, ssl=self.ssl_context, happy_eyeballs_delay=0.25)

    async def event_message(self, message):
        print("Message received: " + message.content)
        data_package = adapt(message)
        self.stream_writer.write(data_package.serialize())
        self.stream_writer.write_eof()
        await self.stream_writer.drain()
        response = await self.stream_reader.readline()
        print("Response received: " + response.decode())
        await message.channel.send(response.decode())

    def get_ssl_context(self):
        return False
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        return ctx


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
