import sys

import aiologger
import aiologger.levels
from aiologger.formatters import base
from aiologger.handlers import streams


def log(cls):
    """A class decorator that adds an async logger factory to the class."""
    cls.logger_factory = get_logger
    return cls


def get_log_handler(config: dict):
    """Returns an aiologger log handler."""
    handler = streams.AsyncStreamHandler(stream=sys.stdout)
    handler.formatter = base.Formatter(
        replace_color_codes(config["logging"]["format"]))
    handler.level = aiologger.levels.LogLevel.DEBUG
    return handler


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def replace_color_codes(string: str):
    """Replaces color codes in a string."""
    return str.format(string,
                      COLOR_HEADER=Colors.HEADER,
                      COLOR_OKBLUE=Colors.OKBLUE,
                      COLOR_OKCYAN=Colors.OKCYAN,
                      COLOR_OKGREEN=Colors.OKGREEN,
                      COLOR_WARNING=Colors.WARNING,
                      COLOR_FAIL=Colors.FAIL,
                      COLOR_ENDC=Colors.ENDC,
                      COLOR_BOLD=Colors.BOLD,
                      COLOR_UNDERLINE=Colors.UNDERLINE)


def get_logger(self: object, config: dict):
    """Returns an aiologger logger."""
    if config["logging"]["enabled"].lower() == "false":
        return FakeAsyncLogger()
    else:
        return get_async_logger(self, config)


class FakeAsyncLogger:
    """A fake async logger that does nothing."""

    async def debug(self, message: str):
        pass

    async def info(self, message: str):
        pass

    async def warning(self, message: str):
        pass

    async def error(self, message: str):
        pass

    async def critical(self, message: str):
        pass

    async def exception(self, message: str):
        pass


def get_async_logger(self: object, config: dict):
    """Returns an aiologger logger."""
    logger = aiologger.Logger()

    if not self:
        logger.name = "root"
    else:
        logger.name = self.__class__.__name__

    logger.add_handler(get_log_handler(config))
    logger.level = aiologger.levels.NAME_TO_LEVEL[config["logging"]["level"]]
    return logger
