import unittest

from bot.DAL.chatter_repository import ChatterRepository
from bot.utils.dependency_injection import Container
from fake_provider import fake


class ChatterRepositoryTests(unittest.TestCase):
    container: Container

    @classmethod
    def setUpClass(cls):
        cls.container = Container()
        cls.container.config.from_yaml('config.yml')
        cls.container.wire(modules=[__name__])

    def setUp(self):
        self.chatter_repo = ChatterRepository(self.container.db())

    def test_find_by_name(self):
        chatters = self.chatter_repo.find(name="owilson")
        chatters = [chatter for chatter in chatters if chatter is not None]
        self.assertTrue(len(chatters) > 0)
        print(f"\ntest_get_chatter: {chatters}")

    def test_insert(self):
        chatter = fake.chatter_entity()
        self.chatter_repo.insert(chatter)
        chatter = self.chatter_repo.find(name=chatter.name)
        self.assertIsNotNone(chatter)

    def test_insert_many(self):
        chatters = []
        for _ in range(1000):
            chatters.append(fake.chatter_entity())

        self.chatter_repo.insert_many(chatters)
        for chatter in chatters:
            chatter = self.chatter_repo.find(name=chatter.name)
            self.assertIsNotNone(chatter)
