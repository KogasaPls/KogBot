import sqlite3

import bot.utils.log
from dependency_injector import containers, providers
from bot.services.auth_service import AuthService
from bot.services.bot_service import BotService
from bot.services.chat_service import ChatService
from bot.services.generator_service import GeneratorService
from bot.services.tokenizer_service import TokenizerService
from bot.utils.init_async import init_async


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=['config.ini'])
    logger = providers.Singleton(bot.utils.log.get_logger, None, config)

    # Gateways
    db = providers.Resource(sqlite3.connect, config.database.dsn)

    auth_service = providers.Singleton(init_async, AuthService, config, db)

    tokenizer_service = providers.Singleton(init_async, TokenizerService,
                                            config, db)

    generator_service = providers.Singleton(init_async, GeneratorService,
                                            config, db)

    chat_service = providers.Singleton(init_async, ChatService, config, db,
                                       tokenizer_service, generator_service)

    bot_service = providers.Factory(init_async, BotService, config, db,
                                    auth_service, chat_service)
