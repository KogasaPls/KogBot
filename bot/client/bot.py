import asyncio
import ssl

from twitchio.ext import commands


class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(token='TOKEN',
                         prefix='?',
                         initial_channels=['CHANNEL'])
        self.ssl_context = self.get_ssl_context()
        self.stream_reader, self.stream_writer = None, None

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        self.stream_reader, self.stream_writer = await asyncio.open_connection(
            '127.0.0.1', 8888, ssl=self.ssl_context, happy_eyeballs_delay=0.25)

    async def event_message(self, message):
        print("Message received: " + message.content)
        self.stream_writer.write(message.content.encode())
        await self.stream_writer.drain()
        self.stream_writer.write_eof()
        response = await self.stream_reader.readline()
        print("Response received: " + response.decode())

    def get_ssl_context(self):
        return False
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        return ctx


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
