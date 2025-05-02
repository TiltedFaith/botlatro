# Imports and global variables
from dotenv import load_dotenv
import os
import discord
import re
import json
from discord.ext import tasks
import time

load_dotenv(dotenv_path='C:\\gian_saucebot\\token.env')
token = os.getenv('DISCORD_TOKEN')


# Global variables and setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
switch = True  # Set the initial state of the switch to True
cooldowns = {}

# Load counters
try:
    with open('good_bot_counter.json', 'r') as file:
        count_data = json.load(file)
except FileNotFoundError:
    count_data = {'goodBotCount': 0}

try:
    with open('bad_bot_counter.json', 'r') as file:
        abuse_data = json.load(file)
except FileNotFoundError:
    abuse_data = {'badBotCount': 0}

# Event handlers
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Legacy event handler for message processing
@client.event
async def on_message(message):
    global switch  # Ensure the `switch` variable is accessible

    if message.author == client.user:
        return  # Ignore messages from the bot itself

    # Blacklist author ID to bypass cooldown
    if message.author.id in [309552034502279169, 1175799826286379183]:
        bypass_cooldown = True
    else:
        bypass_cooldown = False

    # Handle the toggle functionality
    if message.content.startswith('!toggle'):
        switch = not switch
        await message.channel.send(f'Bot is now {"active" if switch else "inactive"}')
        return

    # Handle message forwarding if the bot is active
    if switch:
        if message.channel.id == 1016252482562830346:  # bbq sauce 1
            channel = client.get_channel(1175798186099609610)  # bbq sauce 2
            if message.content:
                await channel.send(message.content)
        elif message.channel.id == 1100418516844285972:  # million scoville 1
            channel = client.get_channel(1175798213769437284)  # million scoville 2
            if message.content:
                await channel.send(message.content)
        elif message.channel.id == 1175798186099609610:  # bbq sauce 2
            channel = client.get_channel(1016252482562830346)  # bbq sauce 1
            if message.content:
                await channel.send(message.content)
        elif message.channel.id == 1175798213769437284:  # million scoville 2
            channel = client.get_channel(1100418516844285972)  # million scoville 1
            if message.content:
                await channel.send(message.content)

    # Handle trigger words with cooldown logic
    user_id = message.author.id
    current_time = time.time()

    if not bypass_cooldown:
        if user_id in cooldowns and current_time - cooldowns[user_id] < 5:
            return  # User is still on cooldown, do nothing

    # Example trigger word handling (add your trigger word logic here)
    await handle_trigger_words(
        message,
        ub_mentioned,
        '<:ub:1178729920730509372>'
    )

    # Update cooldown for non-blacklisted users
    if not bypass_cooldown:
        cooldowns[user_id] = current_time

# Utility functions
async def handle_trigger_words(message, trigger_words, response, cooldown_time=5, exclude_words=None):
    """
    Handles trigger words in a message and sends a response if a trigger word is found.
    Applies a cooldown to prevent spam.

    Args:
        message (discord.Message): The message object from Discord.
        trigger_words (list): A list of trigger words to check in the message.
        response (str): The response string to send if a trigger word is found.
        cooldown_time (int): Cooldown time in seconds for each user. Default is 5 seconds.
    """
    
    # Default exclude_words if not provided
    if exclude_words is None:
        exclude_words = ['ruby', 'yubi', 'philippines', 'karlo', 'himari', 'megumi', 'angelo']
    
    user_id = message.author.id
    current_time = time.time()

    # Check if the user is on cooldown
    if user_id in cooldowns and current_time - cooldowns[user_id] < cooldown_time:
        return  # User is still on cooldown, do nothing
    
    # Check if any excluded word is in the message content
    if exclude_words and any(word in message.content.lower() for word in exclude_words):
        return  # Skip processing if an excluded word is found

    # Check if any trigger word is in the message content
    if any(word in message.content.lower() for word in trigger_words):
        # Ignore messages that are links
        if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
            await message.channel.send(response)
            cooldowns[user_id] = current_time  # Update the cooldown for the user
            
async def handle_trigger_words_image(message, trigger_words, file_path, cooldown_time=5, exclude_words=None):
    """
    Handles trigger words in a message and sends an image file as a response if a trigger word is found.
    Applies a cooldown to prevent spam.

    Args:
        message (discord.Message): The message object from Discord.
        trigger_words (list): A list of trigger words to check in the message.
        file_path (str): The file path of the image to send as a response.
        cooldown_time (int): Cooldown time in seconds for each user. Default is 5 seconds.
        exclude_words (list): A list of words to exclude from triggering. Default is None.
    """
    if exclude_words is None:
        exclude_words = ['ruby', 'yubi', 'philippines', 'karlo', 'himari', 'megumi', 'angelo']

    user_id = message.author.id
    current_time = time.time()

    # Check if the user is on cooldown
    if user_id in cooldowns and current_time - cooldowns[user_id] < cooldown_time:
        return  # User is still on cooldown, do nothing

    # Check if any excluded word is in the message content
    if any(word in message.content.lower() for word in exclude_words):
        return  # Skip processing if an excluded word is found

    # Check if any trigger word is in the message content
    if any(word in message.content.lower() for word in trigger_words):
        # Ignore messages that are links
        if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
            with open(file_path, 'rb') as image_file:
                picture = discord.File(image_file)
                await message.channel.send(file=picture)
                cooldowns[user_id] = current_time  # Update the cooldown for the user


async def handle_trigger_words_video(message, trigger_words, file_path, cooldown_time=5, exclude_words=None):
    """
    Handles trigger words in a message and sends a video file as a response if a trigger word is found.
    Applies a cooldown to prevent spam.

    Args:
        message (discord.Message): The message object from Discord.
        trigger_words (list): A list of trigger words to check in the message.
        file_path (str): The file path of the video to send as a response.
        cooldown_time (int): Cooldown time in seconds for each user. Default is 5 seconds.
        exclude_words (list): A list of words to exclude from triggering. Default is None.
    """
    if exclude_words is None:
        exclude_words = ['ruby', 'yubi', 'philippines', 'karlo', 'himari', 'megumi', 'angelo']

    user_id = message.author.id
    current_time = time.time()

    # Check if the user is on cooldown
    if user_id in cooldowns and current_time - cooldowns[user_id] < cooldown_time:
        return  # User is still on cooldown, do nothing

    # Check if any excluded word is in the message content
    if any(word in message.content.lower() for word in exclude_words):
        return  # Skip processing if an excluded word is found

    # Check if any trigger word is in the message content
    if any(word in message.content.lower() for word in trigger_words):
        # Ignore messages that are links
        if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
            with open(file_path, 'rb') as video_file:
                video = discord.File(video_file)
                await message.channel.send(file=video)
                cooldowns[user_id] = current_time  # Update the cooldown for the user
                return

async def handle_trigger_words_sticker(message, trigger_words, cooldown_time=5):
    """
    Handles stickers in a message and sends a response if a sticker's name matches a trigger word.
    Applies a cooldown to prevent spam.

    Args:
        message (discord.Message): The message object from Discord.
        trigger_words (list): A list of sticker names to check in the message.
        cooldown_time (int): Cooldown time in seconds for each user. Default is 5 seconds.
    """
    user_id = message.author.id
    current_time = time.time()

    # Check if the user is on cooldown
    if user_id in cooldowns and current_time - cooldowns[user_id] < cooldown_time:
        return  # User is still on cooldown, do nothing

    # Check if the message contains stickers
    if message.stickers:
        for sticker in message.stickers:
            # Check if the sticker's name matches any trigger word
            if sticker.name in trigger_words:
                await message.channel.send(sticker.url)  # Send the sticker's URL
                cooldowns[user_id] = current_time  # Update the cooldown for the user
                return
            
ub_mentioned = [
    'm4h1ru', 'mahiru', 'mahiruu', 'mah1ru', 'm4hiru', 'mr m', 'redacted', 'delulu', 
    'kral', 'karl', 'karl angelo reyes', 'karl reyes', 'philip', 'ayaka', 'mr p', 
    'm4h1ruu', 'mah1ruu', 'm4hiruu', 'kr4l', 'k4rl', 'ugly bastard', ':ub:', 'lil bro', 
    'nui', 'mr n', 'mr b', 'bernard', 'tungsten', 'tungstendeagle', 'tungstenfuckface', 
    'fuckface', 'kristian', 'kalansay', 'gelo', 'moraleja', 'gelo moraleja'
]

iyot_mentioned = [
    'iyot', 'eut', 'iot', 'iyut', 'sex', 'cex', 'seks', 'secks', 'cecks', 'ceks', 
    'kantot', 'kantotan', 'kantut', 'kantutan', 'sisig express', 'kanton', 'kantonan', 
    'kantunan', 'canton', 'seggs', 'segg', 'segs', 'eot', 'eyot', 'eyut'
]

raiden_mentioned = [
    'raiden', 'mei', 'acheron', 'makoto', 'baal', 'beelzebub', 'shogun', 'sawashiro', 'miyuki'
]

mika_mentioned = [
    'mika', 'MikaXD', 'XD', 'gorilla', 'xd', 'ayaya', '🦍'
]

posa_mentioned = [
    'pusa', 'posa', 'cat', 'pussy', 'kuting', 'kazusa', 'kikyou', 'serika', 'mari', 'momoi', 'midori', 'akira', 'kirara', 'diona', 'lynette', 'rosmontis'
]

miaw_mentioned = [
    'miaw', 'meow', 'nyan'
]

elf_mentioned = [
    'elysia', 'iori', 'frieren', 'nanagami rin', 'junko', 'chinatsu', 'ayane', 
    'muelsyse', 'mumu', 'aomori mine', 'megu', 'himari', 'preyren', 'layla', 'oki aoi'
]

alya_char_mentioned = [
    'alya', 'alisa', 'mikhailovna'
]

pekeng_posa_char_mentioned = [
    'shiroko'
]

rumi_mentioned = [
    'rumi'
]

ichika_mentioned = [
    'ichika'
]

baubau_mentioned = [
    'baubau', 'bau bau', 'fuwamoco', 'fuwawa', 'mococo', 'hibiki', 'ceobe'
]

korone_mentioned = [
    'korone', 'yubi', 'koone'
]

ruby_mentioned = [
    'ruby'
]

daga_mentioned = [
    'daga', 'rat', 'rrat'
]

topaz_mentioned = [
    'topaz'
]

ogey_mentioned = [
    'ogey', 'ogei'
]

tikoy_mentioned = [
    'loli', 'uo', 'uoh', 'cunny', 'cnuuy', 'cnnuy', 'kani', '😭', '🦀'
]

bocchi_mentioned = [
    'bocchi', 'hitori goto', 'hitori gotoh', 'hitori gotou', 'bocc', 'bocchers', 
    'hitori', 'gotoh', 'gotou'
]

sadhamster_mentioned = [
    ':sadhamster:'
]

yuuka_mentioned = [
    'yuuka'
]

jarvis_mentioned = [
    'jarvis', 'jabol', 'jakol'
]


menhera_mentioned = [
    'menhera'
]

gojo_mentioned = [
    'gojo'
]

byakuya_mentioned = [
    'byakuya'
]

kys_mentioned = [
    'i want to die', 'i want to kill myself', 'i want to kms', 'i wanna kms', 
    'i wanna kill myself', 'kys', 'keep yourself safe'
]

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    # Handle ub_mentioned trigger words
    await handle_trigger_words(
        message, 
        ub_mentioned, 
        '<:ub:1178729920730509372>'
    )

    # Handle iyot_mentioned trigger words
    await handle_trigger_words(
        message, 
        iyot_mentioned, 
        'iyot mentioned'
    )
    
    if message.guild.id != 1014113663499649045:
        await handle_trigger_words(
            message,
            raiden_mentioned,
            'so bakit nga ba RK'
        )

    # Handle mika_mentioned trigger words
    await handle_trigger_words(
        message, 
        mika_mentioned, 
        '<:MikaXD:1179436633779613696>'
    )

    # Handle posa_mentioned trigger words
    await handle_trigger_words(
        message, 
        posa_mentioned, 
        'posa <:bocchi_ehehe:1179447995931049984>',
        exclude_words=['himari']
    )

    # Handle miaw_mentioned trigger words
    await handle_trigger_words(
        message, 
        miaw_mentioned, 
        '<:miaw:1179606920693305467>'
    )

    # Handle alya_char_mentioned trigger words
    await handle_trigger_words(
        message, 
        alya_char_mentioned, 
        'alya <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle pekeng_posa_char_mentioned trigger words
    await handle_trigger_words(
        message, 
        pekeng_posa_char_mentioned, 
        'pekeng posa <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle rumi_mentioned trigger words
    await handle_trigger_words(
        message, 
        rumi_mentioned, 
        'rumi <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle ichika_mentioned trigger words
    await handle_trigger_words(
        message, 
        ichika_mentioned, 
        'ichika <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle baubau_mentioned trigger words
    await handle_trigger_words(
        message, 
        baubau_mentioned, 
        'baubau <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle korone_mentioned trigger words
    await handle_trigger_words(
        message, 
        korone_mentioned, 
        'yubi yubi <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle ruby_mentioned trigger words
    await handle_trigger_words(
        message, 
        ruby_mentioned, 
        'ruby <:bocchi_ehehe:1179447995931049984>'
    )

    # Handle daga_mentioned trigger words
    await handle_trigger_words(
        message, 
        daga_mentioned, 
        '🖕🐀'
    )

    # Handle topaz_mentioned trigger words
    await handle_trigger_words(
        message, 
        topaz_mentioned, 
        '🍑 just tell everyone on our team 🍑'
    )

    # Handle ogey_mentioned trigger words
    await handle_trigger_words(
        message, 
        ogey_mentioned, 
        'rrat'
    )

    # Handle tikoy_mentioned trigger words
    await handle_trigger_words(
        message, 
        tikoy_mentioned, 
        '😭'
    )

    # Handle bocchi_mentioned trigger words
    await handle_trigger_words(
        message, 
        bocchi_mentioned, 
        '<:bocchi_ehehe:1179447995931049984>'
    )

    # Handle sadhamster_mentioned trigger words
    await handle_trigger_words(
        message, 
        sadhamster_mentioned, 
        '<:sadhamster:1211275120375496734>'
    )

    # Handle elf_mentioned trigger words
    await handle_trigger_words_image(
        message, 
        elf_mentioned, 
        r'C:\gian_saucebot\images\iyot.png'
    )
    
    # Handle yuuka_mentioned trigger words
    await handle_trigger_words_image(
        message, 
        yuuka_mentioned, 
        r'C:\gian_saucebot\images\yuuka.png'
    )
    
    # Handle jarvis_mentioned trigger words
    await handle_trigger_words_image(
        message, 
        jarvis_mentioned, 
        r'C:\gian_saucebot\images\jarvis.png'
    )

    # Handle menhera_mentioned trigger words
    await handle_trigger_words_image(
        message, 
        menhera_mentioned, 
        r'C:\gian_saucebot\images\MikaSurprised.png'
    )

    # Handle gojo_mentioned trigger words
    await handle_trigger_words_image(
        message, 
        gojo_mentioned, 
        r'C:\gian_saucebot\images\gojo_reaction.gif'
    )

    # Handle byakuya_mentioned trigger words
    await handle_trigger_words_image(
        message, 
        byakuya_mentioned, 
        r'C:\gian_saucebot\images\byakuya.jpg'
    )
    
    # Handle menhera_mentioned trigger words
    await handle_trigger_words_video(
        message, 
        kys_mentioned, 
        r'C:\gian_saucebot\images\dont_kys.mp4'
    )
    
    # Handle stickers named "MIAW"
    await handle_trigger_words_sticker(
        message,
        ['MIAW']
    )

    # Handle stickers named "niggasaki"
    await handle_trigger_words_sticker(
        message,
        ['niggasaki']
    )

    goodBot_mentioned = ['good bot']
    if any(word in message.content.lower() for word in goodBot_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    count_data['goodBotCount'] += 1
                    await message.add_reaction('<:bocchi_hehe:1179606498893123634>')
                    await client.change_presence(activity=discord.Game(name=f"Appreciated {count_data['goodBotCount']} times and abused  {abuse_data['badBotCount']} times"))
                    cooldowns[message.author.id] = time.time()
                    return
                
    with open('good_bot_counter.json', 'w') as file:
                json.dump({'goodBotCount': count_data['goodBotCount']}, file)

    badBot_mentioned = ['bad bot']
            # reactions = ['😭', '<:bocchi_nervous:1184157795927466176>', '<:ambatukam_sad:1184157785169068082>', '<:sad_cat:1184157807113666590>', '<:troll_sad:1184157817301635122>']
    if any(word in message.content.lower() for word in badBot_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    abuse_data['badBotCount'] += 1
                    with open(r'C:\gian_saucebot\images\Ruby_Bonk.gif', 'rb') as ruby:
                        pictureRuby = discord.File(ruby)
                        await message.channel.send(file=pictureRuby)
                    # for reaction in reactions:
                    #     await message.add_reaction(reaction)
                        await client.change_presence(activity=discord.Game(name=f"Appreciated {count_data['goodBotCount']} times and abused {abuse_data['badBotCount']} times"))
                        cooldowns[message.author.id] = time.time()
                
    with open('bad_bot_counter.json', 'w') as file:
                json.dump({'badBotCount': abuse_data['badBotCount']}, file)


client.run(token)