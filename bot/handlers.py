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

        msg_lower = message.content.lower()

        # Check cooldown first
        if not await handler.handle_message(message):
            return
        
        # ==========VOICE COMMANDS==========
        if message.content.startswith("!join"):
            await handler.join_voice(message)

        elif message.content.startswith("!leave"):
            await handler.leave_voice(message.guild.id)
        
        # ==========TEXT COMMANDS==========
        # B-KOMACHI
        if any(keyword in msg_lower for keyword in [
            'b-komachi', 'bkomachi', 'b komachi', 
            'gsc komachi', 'gsc bkomachi', 'gsc-komachi'
        ]):  
            print("Triggered 'komachi' response")
            await message.channel.send('https://tenor.com/view/oshi-no-ko-b-komachi-hoshino-ruby-arima-kana-mem-cho-gif-442194686914760108')
            return

        # ==========FILE COMMANDS==========
        # BALATRO
        if 'balatro' in msg_lower:
            print("Triggered 'balatro' image")
            balatro_path = Path(__file__).parent.parent/'assets'/'images'/'balatro.jpg'
            try:
                with open(balatro_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find the balatro image!")
                print(f"Image not found at: {balatro_path}")
            return
        
        # GROS MICHEL
        if 'gros michel' in msg_lower or 'cavendish' in msg_lower:
            print("Triggered 'gros michel' image")
            banana_path = Path(__file__).parent.parent/'assets'/'images'/'banana.webp'
            try:
                with open(banana_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find the gros michel image!")
                print(f"Image not found at: {banana_path}")
            return

        # BAD BOT
        if 'bad bot' in msg_lower:
            print("Triggered 'bad bot' image")
            badbot_path = Path(__file__).parent.parent/'assets'/'images'/'bad bot.jpg'
            try:
                with open(badbot_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find the bad bot image!")
                print(f"Image not found at: {badbot_path}")
            return
        
        # GOOD BOT
        if 'good bot' in msg_lower:
            print("Triggered 'good bot' image")
            goodbot_path = Path(__file__).parent.parent/'assets'/'images'/'good bot.jpg'
            try:
                with open(goodbot_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find the good bot image!")
                print(f"Image not found at: {goodbot_path}")
            return
        
        # SA CUBAO
        if 'cubao' in msg_lower:
            print("Triggered 'cubao' audio")
            cubao_path = Path(__file__).parent.parent / 'assets' / 'audio' / 'Sa cubao.mp3'
            try:
                audio_file = discord.File(cubao_path)
                await message.channel.send(file=audio_file)
            except FileNotFoundError:
                await message.channel.send("Couldn't find the cubao audio!")
                print(f"Audio not found at: {cubao_path}")
            except discord.HTTPException as e:
                await message.channel.send(f"Failed to send audio: {e}")
                print(f"Audio send error: {e}")
            return
        
        # LEAGUE OF LEGENDS
        if any(keyword in msg_lower for keyword in [
            'league', 'league of legends']):
            print("Triggered 'league' video")
            league_path = Path(__file__).parent.parent / 'assets' / 'video' / 'Stinky.mp4'
            try:
                video_file = discord.File(league_path)
                await message.channel.send(file=video_file)
            except FileNotFoundError:
                await message.channel.send("Couldn't find the league video!")
                print(f"Video not found at: {video_file}")
            except discord.HTTPException as e:
                await message.channel.send(f"Failed to send video: {e}")
                print(f"Audio send error: {e}")
            return
        
        # JUMPSCARE
        if 'jumpscare' in msg_lower:
            print("Triggered 'jumpscare' image")
            jumpscare_path = Path(__file__).parent.parent/'assets'/'images'/'jumpscare.png'
            try:
                with open(jumpscare_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find jumpscare image!")
                print(f"Image not found at: {jumpscare_path}")
            return