import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv('.env')
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        
        if not self.TOKEN:
            raise ValueError("No token found in .env file")

        self.INTENTS = discord.Intents.default()
        self.INTENTS.message_content = True