from bot.services.interfaces import (IAuthService, IBotService,
                                     IChatMessageService, IGeneratorService,
                                     ITokenizerService)


class BotService(IBotService):
    auth_service: IAuthService
    generator_service: IGeneratorService
    tokenizer_service: ITokenizerService
    chat_message_service: IChatMessageService

    def __init__(self, config: dict, auth_service: IAuthService,
                 generator_service: IGeneratorService,
                 chat_message_service: IChatMessageService):
        super().__init__(config)
        self.auth_service = auth_service
        self.generator_service = generator_service
        self.chat_message_service = chat_message_service

    async def run(self):
        print("Hello, world!")
