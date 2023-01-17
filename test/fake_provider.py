from faker import Faker
from faker.providers import BaseProvider
from bot.models.chat_message import ChatMessage
from bot.models.chat_room import ChatRoom
from bot.models.chatter import Chatter

fake = Faker()


class FakeProvider(BaseProvider):

    def chat_room(self):
        id = self.random_int()
        name = fake.user_name()

        chat_room = ChatRoom()
        chat_room.id = id
        chat_room.name = name
        return chat_room

    def chatter(self):
        id = self.random_int()
        name = fake.user_name()

        chatter = Chatter()
        chatter.id = id
        chatter.name = name
        return chatter

    def chat_message(self):
        id = self.random_int()
        chatter = self.chatter()
        chat_room = self.chat_room()
        message_text = fake.text()
        sent_at_time = fake.date_time()

        message = ChatMessage()
        message.id = id
        message.chatter = chatter
        message.chat_room = chat_room
        message.message = message_text
        message.sent_at_time = sent_at_time
        return message


fake.add_provider(FakeProvider)
