import asyncio

import twitchio
from dotenv import dotenv_values
from twitchio.ext import commands
from bot.models.chat_message import ChatMessage
from bot.models.chat_room import ChatRoom
from bot.models.chatter import Chatter


def adapt(message: twitchio.Message) -> ChatMessage | None:
    if message.echo:
        return None

    chatter = Chatter(message.author.name)
    chat_room = ChatRoom(message.channel.name)
    return ChatMessage(chatter, chat_room, message.content, message.timestamp)


def try_adapt(message: twitchio.Message) -> ChatMessage | None:
    try:
        return adapt(message)
    except Exception as e:
        print(e)
        return None


class TwitchBot(commands.Bot):

    def __init__(self):
        config = dotenv_values(".env")
        super().__init__(token=config["TWITCH_TOKEN"],
                         prefix='?',
                         initial_channels=[config["TWITCH_CHANNEL"]])
        self.stream_reader, self.stream_writer = None, None

    async def event_ready(self):
        print(f'Logged in as {self.nick}')
        self.stream_reader, self.stream_writer = await asyncio.open_connection(
            '127.0.0.1', 8888)

    async def event_message(self, msg: twitchio.Message):
        try:
            response = await self.handle_message_and_get_response(msg)
            if response is not None:
                await msg.channel.send(response)
        except Exception as e:
            print(e)

    async def handle_message_and_get_response(
            self, msg: twitchio.Message) -> str | None:
        chat_message: ChatMessage = try_adapt(msg)
        if chat_message is None:
            return

        print(chat_message.__repr__())

        data = chat_message.serialize()
        self.stream_writer.write(data)
        await self.stream_writer.drain()

        response = await self.try_get_response()
        if response is None:
            return

        await msg.channel.send(response)

    async def try_get_response(self) -> str | None:
        try:
            response = (await self.stream_reader.readline()).decode()
            print("Response received: " + response)
            return response
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
