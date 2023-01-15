import unittest

from bot.services.interfaces import IChatService
from bot.utils.dependency_injection import Container
from fake_provider import get_fake_chat_message


class ChatServiceTests(unittest.IsolatedAsyncioTestCase):
    container: Container

    @classmethod
    def setUpClass(cls):
        cls.container = Container()
        cls.container.config.from_yaml('config.yml')
        cls.container.wire(modules=[__name__])

    async def asyncSetUp(self):
        self.chat_service: IChatService = await self.container.chat_service()

    async def test_get_reply(self):
        message = get_fake_chat_message()
        out: str = await self.chat_service.get_response(message)
        self.assertIsNotNone(out)
        print(f"\ntest_get_reply: {out}")
