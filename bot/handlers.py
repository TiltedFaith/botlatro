import os
import discord
import time
from pathlib import Path
import random
import sqlite3

class MessageHandler:
    def __init__(self, client):
        self.client = client
        self.user_cooldowns = {}  # {user_id: last_message_time}
        self.cooldown = 3  # seconds
        self.voice_clients = {}  # {guild_id: voice_client}
        self.db = sqlite3.connect('gacha_data.db', check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                gacha_counter INTEGER DEFAULT 0,
                guarantee_counter INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pull_history (
                user_id INTEGER,
                pull_result TEXT,
                pull_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db.commit()

    async def close(self):
        """Call this when the bot shuts down"""
        self.db.close()

    async def update_user_counters(self, user_id, gacha_counter, guarantee_counter):
        try:
            cursor = self.db.cursor()
            cursor.execute('BEGIN TRANSACTION')  # Start transaction
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                VALUES (?, ?, ?)
            ''', (user_id, gacha_counter, guarantee_counter))
            self.db.commit()  # Commit on success
        except Exception as e:
            self.db.rollback()  # Rollback on error
            raise e

    async def log_pull(self, user_id, result):
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO pull_history (user_id, pull_result)
            VALUES (?, ?)
        ''', (user_id, result))
        self.db.commit()

    async def get_user_counters(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT gacha_counter, guarantee_counter FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return row or (0, 0)  # Default to 0 if user doesn't exist

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
        if any(keyword in msg_lower for keyword in ['b-komachi', 'bkomachi', 'b komachi', 'gsc komachi', 'gsc bkomachi', 'gsc-komachi']):  
            print("Triggered 'komachi' response")
            await message.channel.send('https://tenor.com/view/oshi-no-ko-b-komachi-hoshino-ruby-arima-kana-mem-cho-gif-442194686914760108')
            return
        
        if any(keyword in msg_lower for keyword in ['i love botlatro', 'i love you botlatro', 'i love you, botlatro', 'i love <@1368022942687953026>', 'i love you <@1368022942687953026>', 'i love you, <@1368022942687953026>', 'i love botlatro <@1368022942687953026>', 'i love you botlatro <@1368022942687953026>', 'i love you, botlatro <@1368022942687953026>']):
            print("Triggered 'I love botlatro' response")
            await message.channel.send('https://tenor.com/view/green-goblin-tongue-malicious-devious-gif-24541958')
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
        if any(keyword in msg_lower for keyword in ['league', 'league of legends']):
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
        
        # JOKER
        if any(keyword in msg_lower for keyword in ['joker','jimbo']): 
            print("Triggered 'joker' image")
            joker_path = Path(__file__).parent.parent/'assets'/'images'/'joker.png'
            try:
                with open(joker_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find joker image!")
                print(f"Image not found at: {joker_path}")
            return
        
        # WHEEL OF FORTUNE
        if 'wheel of fortune' in msg_lower:
            wheeloffortune_path = ""
            print("Triggered 'wheel of fortune' image")
            def get_card_style():
                styles = ["nope", "foil", "holographic", "polychrome"]
                weights = [75.0, 12.5, 8.75, 3.75]
                return random.choices(styles, weights=weights, k=1)[0]
            
            match get_card_style():
                case "nope":
                    wheeloffortune_path = Path(__file__).parent.parent/'assets'/'images'/'nope.png'
                case "foil":
                    wheeloffortune_path = Path(__file__).parent.parent/'assets'/'images'/'foil.webp'
                case "holographic":
                    wheeloffortune_path = Path(__file__).parent.parent/'assets'/'images'/'holographic.webp'
                case "polychrome":
                    wheeloffortune_path = Path(__file__).parent.parent/'assets'/'images'/'polychrome.webp'

            try:
                with open(wheeloffortune_path, 'rb') as img:
                    await message.channel.send(file=discord.File(img))
            except FileNotFoundError:
                await message.channel.send("Couldn't find wheel of fortune image!")
                print(f"Image not found at: {wheeloffortune_path}")
            
        #============GACHA===========
        def get_rates(gacha_counter, guarantee_counter):
            ssr = 0.6  # Base SSR rate (5★)
            sr = 5.1    # Base SR rate (4★)
            normal = 94.3  # Base Normal rate (3★)
            # Apply 4★ guarantee if needed
            if guarantee_counter >= 10:
                return {
                    "ssr_rate": ssr,
                    "non_ssr_rate": 100 - ssr,  # All non-SSR becomes SR
                    "non_ssr": {
                        "sr_rate": 100 - ssr,   # 100% of non-SSR is SR
                        "normal_rate": 0         # 0% chance for Normal
                    }
                }
            
            # Apply progressive pity after 74 pulls
            if gacha_counter > 74:
                increase = (gacha_counter - 74) * 6
                ssr = min(100, ssr + increase)
                remaining = 100 - ssr

                # Maintain original SR/Normal ratio
                original_sr_ratio = sr / (sr + normal)
                sr = remaining * original_sr_ratio
                normal = remaining * (1 - original_sr_ratio)
            
            non_ssr = sr + normal
            return {
                "ssr_rate": ssr,
                "non_ssr_rate": non_ssr,
                "non_ssr": {
                    "sr_rate": sr,
                    "normal_rate": normal
                }
            }        
        async def counter_message(user_id):
            gacha_counter, guarantee_counter = await handler.get_user_counters(user_id)

            gacha_counter_msg = f"Guaranteed 5 Star!: {90 - gacha_counter}"
            guarantee_counter_msg = f"Guaranteed 4 Star!: {10 - guarantee_counter}"

            return await message.channel.send(
                f"{message.author.mention}\n{gacha_counter_msg}\n{guarantee_counter_msg}"
            )
            """Generate and send HTML galleries for all rarities"""
            try:
                rarities = ['3 star', '4 star', '5 star']
                files = []
                
                for rarity in rarities:
                    try:
                        html_path = generate_html_for_rarity(rarity)
                        files.append(discord.File(html_path, filename=f"{rarity.replace(' ', '_')}_gallery.html"))
                    except FileNotFoundError as e:
                        print(f"Couldn't generate gallery for {rarity}: {e}")
                        await message.channel.send(f"Couldn't generate gallery for {rarity}")

                if files:
                    await message.channel.send(
                        f"{message.author.mention} Here are the gacha item galleries:",
                        files=files
                    )
                    
                    # Clean up temporary files
                    for file in files:
                        try:
                            Path(file.filename).unlink()
                        except:
                            pass
                else:
                    await message.channel.send("Couldn't generate any galleries.")
                    
            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")
                print(f"Error generating galleries: {e}")
        
        if msg_lower.startswith('!gachapool'):
            await message.channel.send("List of gacha pools can be found here: https://github.com/TiltedFaith/botlatro/tree/main/assets/images/gacha\n")
        # GACHA COUNTER
        if msg_lower.startswith('!counter'):
            user_id = message.author.id
            await counter_message(user_id)
            
        # HOYO GACHA PULL
        if msg_lower.startswith('!hoyogacha'):
            user_id = message.author.id
            gacha_counter, guarantee_counter = await handler.get_user_counters(user_id)
            pull_count = 1
            
            # 10 PULLS
            if msg_lower.startswith('!hoyogacha10'):
                pull_count = 10

            results = []
            
            for _ in range(pull_count):
                gacha_counter += 1 
                guarantee_counter += 1

                current_rates = get_rates(gacha_counter, guarantee_counter)
                
                def pull():
                    styles = ["5star", "4star", "3star"]
                    weights = [
                        current_rates["ssr_rate"],              
                        current_rates["non_ssr"]["sr_rate"],    
                        current_rates["non_ssr"]["normal_rate"]
                    ]
                    return random.choices(styles, weights=weights, k=1)[0]
                
                result = pull()
                results.append(result)
                
                # Update counters if needed
                if result == "5star":
                    gacha_counter = 0
                    guarantee_counter = 0
                elif result == "4star":
                    guarantee_counter = 0

            await handler.update_user_counters(user_id, gacha_counter, guarantee_counter)

            await counter_message(user_id)

            # Get and send images
            def get_random_image(folder):
                """Get a random image (.webp, .png, .jpg) from the specified folder."""
                folder_path = Path(__file__).parent.parent / 'assets' / 'images' / 'gacha' / folder
                if not folder_path.exists():
                    raise FileNotFoundError(f"Folder not found: {folder_path}")

                # Find all allowed image formats (case-insensitive)
                allowed_extensions = ('.webp', '.png', '.jpg')
                images = [
                    img for img in folder_path.iterdir()
                    if img.suffix.lower() in allowed_extensions and img.is_file()
                ]

                if not images:
                    raise FileNotFoundError(f"No images (webp/png/jpg) found in {folder_path}")

                return random.choice(images)

            # For 10-pull, we'll send all images in one message
            files = []
            for result in results:
                try:
                    match result:
                        case "5star":
                            image_path = get_random_image('5 star')
                            print("5 star gacha pulled!")
                            await message.channel.send(f"{message.author.mention} 5 star gacha pulled!")
                        case "4star":
                            image_path = get_random_image('4 star')
                            print("4 star gacha pulled!")
                            await message.channel.send(f"{message.author.mention} 4 star gacha pulled!")
                        case "3star":
                            image_path = get_random_image('3 star')
                            print("3 star gacha pulled!")
                    await handler.log_pull(user_id, result)  # Log each pull
                    files.append(discord.File(image_path))
                except FileNotFoundError:
                    print(f"Image not found for result: {result}")

            if files:
                await message.channel.send(f"{message.author.mention}", files=files)
            else:
                await message.channel.send("Couldn't find any gacha images!")

        # ==========COMMAND LIST==========
        if msg_lower.startswith('!commands'):
            commands = [
                "!join - Join your voice channel (no functionality yet)",
                "!leave - Leave your voice channel (no functionality yet)",
                "!counter - Check your gacha counter",
                "!hoyogacha - Single pull",
                "!hoyogacha10 - 10 pulls",
                "!commands - List all commands"
                "!gachapool - List all gacha pools",
            ]
            await message.channel.send(f"{message.author.mention} \n" + f"\n".join(commands))