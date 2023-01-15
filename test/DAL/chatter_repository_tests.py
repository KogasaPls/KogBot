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

    def test_get_chatter_by_name(self):
        chatter = self.chatter_repo.get_chatter_by_name("KogasaPls")
        self.assertIsNotNone(chatter)
        print(f"\ntest_get_chatter: {chatter}")

    def test_create_chatter(self):
        chatter = fake.chatter()
        self.chatter_repo.create(chatter)
        chatter = self.chatter_repo.get_chatter_by_name(chatter.name)
        self.assertIsNotNone(chatter)
