from entities.chat.chat_message import ChatMessage
from entities.chat.chat_room import ChatRoom
from entities.chat.chatter import Chatter

from faker.providers import BaseProvider
from faker import Faker


class FakeProvider(BaseProvider):

    def chat_room(self):
        id = self.random_int()
        name = self.name()
        return ChatRoom(id, name)

    def chatter(self):
        id = self.random_int()
        name = self.name()
        return Chatter(id, name)

    def chat_message(self):
        sender = self.get_fake_chatter()
        chat_room = self.get_fake_chat_room()
        message = self.text(30)
        return ChatMessage(sender, chat_room, message)


fake = Faker()
fake.add_provider(FakeProvider)
