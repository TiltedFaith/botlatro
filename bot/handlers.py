import os
import discord
import time
from pathlib import Path

class MessageHandler:
    def __init__(self, client):
        self.client = client
        self.user_cooldowns = {}  # {user_id: last_message_time}
        self.cooldown = 3  # seconds

    async def handle_message(self, message):
        current_time = time.time()
        user_id = message.author.id

        # Cooldown check
        if user_id in self.user_cooldowns:
            elapsed = current_time - self.user_cooldowns[user_id]
            if elapsed < self.cooldown:
                return False  # Message blocked by cooldown

        # Update cooldown
        self.user_cooldowns[user_id] = current_time
        return True  # Message allowed

def setup_handlers(client):
    handler = MessageHandler(client)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        print(f"Received message: {message.content}")

        # Check cooldown first
        if not await handler.handle_message(message):
            return

        # BALATRO IMAGE
        balatro_path = Path(__file__).parent.parent/'assets'/'images'/'balatro.jpg'
        
        if message.content.lower() == 'balatro':
            print("Triggered 'balatro' image")
            try:
                with open(balatro_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find the balatro image!")
                print(f"Image not found at: {balatro_path}")
                return

        '''
        # YE RESPONSE (commented out)
        if message.content.lower() == 'ye':
            print("Triggered 'ye' response")
            await message.channel.send('ye')
        '''