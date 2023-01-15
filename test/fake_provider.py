from faker import Faker
from faker.providers import BaseProvider
from entities.chat.chat_message import ChatMessage
from entities.chat.chat_room import ChatRoom
from entities.chat.chatter import Chatter

fake = Faker()


class FakeProvider(BaseProvider):

    def chat_room(self):
        id = self.random_int()
        name = fake.name()
        return ChatRoom(id, name)

    def chatter(self):
        id = self.random_int()
        name = fake.name()
        return Chatter(id, name)

    def chat_message(self):
        sender = self.chatter()
        chat_room = self.chat_room()
        message = fake.text(30)
        return ChatMessage(sender, chat_room, message)


fake.add_provider(FakeProvider)
