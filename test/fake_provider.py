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
        name = fake.user_name()
        chatter = Chatter()
        chatter.id = id
        chatter.name = name
        return chatter

    def chat_message(self):
        sender = self.chatter()
        chat_room = self.chat_room()
        text = fake.text(30)
        sent_at_time = fake.date_time()
        message = ChatMessage()
        message.sender = sender
        message.chat_room = chat_room
        message.message = text
        message.sent_at_time = sent_at_time
        return message


fake.add_provider(FakeProvider)
