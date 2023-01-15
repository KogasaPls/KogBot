import unittest

from faker import Faker
from bot.utils.dependency_injection import Container

from fake_provider import FakeProvider

container = Container()
container.config.from_yaml('config.yml')
container.wire(modules=[__name__])

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_loader = unittest.TestLoader()
    suite = test_loader.discover(start_dir='test', pattern='*_tests.py')
    fake = Faker()
    fake.add_provider(FakeProvider)
    runner.run(suite)
