import discord
from .handlers import setup_handlers
from config import Config

class BotClient(discord.Client):
    def __init__(self, config):
        super().__init__(intents=config.INTENTS)
        self.config = config
        setup_handlers(self)

    async def on_ready(self):
        print(f'Bot is ready as {self.user}')
        await self.change_presence(
            activity=discord.Game(name="Say 'ye' to me!")
        )