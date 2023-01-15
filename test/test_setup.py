import unittest

container = bot.structure.containers.Container()
container.config.from_yaml('config.yml')
container.wire(modules=[__name__])

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_loader = unittest.TestLoader()
    suite = test_loader.discover(start_dir='test', pattern='*_tests.py')
    runner.run(suite)
