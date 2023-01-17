import unittest

from bot.DAL.repos.chat_message_repository import ChatMessageRepository
from bot.utils.dependency_injection import Container
from fake_provider import fake


class ChatMessageRepositoryTests(unittest.TestCase):
    container: Container

    @classmethod
    def setUpClass(cls):
        cls.container = Container()
        cls.container.config.from_yaml('config.yml')
        cls.container.wire(modules=[__name__])

    def setUp(self):
        self.chat_message_repo = ChatMessageRepository(self.container.db())

    def test_insert(self):
        message = fake.chat_message()
        self.chat_message_repo.insert(message)

    def test_insert_many(self):
        chat_messages = []
        for _ in range(1000):
            message = fake.chat_message()
            chat_messages.append(message)

        self.chat_message_repo.insert_many(chat_messages)

    def test_find_by_id(self):
        message = fake.chat_message()
        self.chat_message_repo.insert(message)
        found = self.chat_message_repo.find(id=message.id)[0]
        self.assertIsNotNone(found)
        self.assertTrue(hasattr(found, "id"))
        self.assertEqual(message.id, found.id)
