import os
import discord
import time
from pathlib import Path

class MessageHandler:
    def __init__(self, client):
        self.client = client
        self.user_cooldowns = {}  # {user_id: last_message_time}
        self.cooldown = 3  # seconds
        self.voice_clients = {}  # {guild_id: voice_client}

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

    async def join_voice(self, message):
        """Join the author's voice channel"""
        if not message.author.voice:
            await message.channel.send("You're not in a voice channel!")
            return False

        voice_channel = message.author.voice.channel
        guild_id = message.guild.id

        # If already connected to this guild
        if guild_id in self.voice_clients:
            await self.voice_clients[guild_id].move_to(voice_channel)
            return True

        try:
            vc = await voice_channel.connect()
            self.voice_clients[guild_id] = vc
            return True
        except Exception as e:
            await message.channel.send(f"Failed to join: {str(e)}")
            return False

    async def leave_voice(self, guild_id):
        """Leave voice channel in specified guild"""
        if guild_id in self.voice_clients:
            await self.voice_clients[guild_id].disconnect()
            del self.voice_clients[guild_id]
            return True
        return False

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
        
        # ==========VOICE COMMANDS==========
        if message.content.startswith("!join"):
            await handler.join_voice(message)

        elif message.content.startswith("!leave"):
            await handler.leave_voice(message.guild.id)

        # ==========FILE COMMANDS==========
        # BALATRO
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
        
        # ==========TEXT COMMANDS==========
        # B-KOMACHI
        if (message.content.lower() == 'b-komachi' or message.content.lower() == 'bkomachi' or message.content.lower() == 'b komachi' or message.content.lower() == 'gsc komachi' or message.content.lower() == 'gsc bkomachi' or message.content.lower() == 'gsc-komachi'):
            print("Triggered 'komachi' response")
            await message.channel.send('https://tenor.com/view/oshi-no-ko-b-komachi-hoshino-ruby-arima-kana-mem-cho-gif-442194686914760108')
