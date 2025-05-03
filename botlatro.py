import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('token.env')
token = os.getenv('DISCORD_TOKEN')

# Initialize client with default intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == client.user:
        return
    
    # Check if message is "ye" (case insensitive)
    if message.content.lower() == 'ye':
        await message.channel.send('wee')

# Run the bot
client.run(token)