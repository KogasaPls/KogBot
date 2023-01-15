import unittest

from utils.dependency_injection import Container


class GeneratorServiceTests(unittest.IsolatedAsyncioTestCase):

    container: Container

    @classmethod
    def setUpClass(cls):
        cls.container = Container()
        cls.container.config.from_yaml('config.yml')
        cls.container.wire(modules=[__name__])

    async def asyncSetUp(self):
        service = await self.container.generator_service()
        self.generator_service = service

    async def test_generate_async(self):
        out = await self.generator_service.generate_async("Hello!")
        self.assertIsNotNone(out)
        print(f"\ntest_generate_async: {out}")
