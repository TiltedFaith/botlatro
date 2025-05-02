import discord
import re
import json
# import os
from discord.ext import tasks
# from dotenv import load_dotenv
import time


# load_dotenv()

# bot_token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
switch = True  # Set the initial state of the switch to True

cooldowns = {}

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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name=f"Appreciated {count_data['goodBotCount']} times and abused {abuse_data['badBotCount']} times"))

@client.event
async def on_message(message):
    global switch
    if message.author.id == 309552034502279169:  # ako to

        if message.content.startswith('!toggle'):
            switch = not switch
            await message.channel.send(f'Bot is now {"active" if switch else "inactive"}')
        if switch:
            if message.channel.id == 1016252482562830346:  # bbq sauce 1
                channel = client.get_channel(1175798186099609610)  # bbq sauce 2
                if message.content:
                    await channel.send(message.content)
            if message.channel.id == 1100418516844285972:  # million scoville 1
                channel = client.get_channel(1175798213769437284)  # million scoville 2
                if message.content:
                    await channel.send(message.content)
            if message.channel.id == 1175798186099609610:  # bbq sauce 2
                channel = client.get_channel(1016252482562830346)  # bbq sauce 1
                if message.content:
                    await channel.send(message.content)
            if message.channel.id == 1175798213769437284:  # million scoville 2
                channel = client.get_channel(1100418516844285972)  # million scoville 1
                if message.content:
                    await channel.send(message.content)

    if message.guild.id != 1014113663499649045: # da boys server
        raiden_mentioned = ['raiden', 'mei', 'acheron', 'makoto', 'baal', 'beelzebub', 'shogun', 'sawashiro', 'miyuki']
        if any(word in message.content.lower() for word in raiden_mentioned):
            await message.channel.send('so bakit nga ba RK')
            cooldowns[message.author.id] = time.time()
            return

    if message.author.id != 1175799826286379183:

        if message.author.id != 309552034502279169 and message.author.id in cooldowns and time.time() - cooldowns[message.author.id] < 5:
            return
        else:

            if message.content.startswith('!ping'):
                await message.channel.send(f'Pong! I am currently {"active" if switch else "inactive"}')
                cooldowns[message.author.id] = time.time()
                return

            if message.content.startswith('!goodnight'):
                await message.channel.send(f'||good|| nig||ht|| g||am||ers')
                cooldowns[message.author.id] = time.time()
                return
            
            elif message.content.startswith('!goodmorning'):
                await message.channel.send(f'||good mor||ni||n||g g||am||ers')
                cooldowns[message.author.id] = time.time()
                return

            elif message.content.startswith('!suso'):
                await message.channel.send(f'Suso ni Preyren')
                cooldowns[message.author.id] = time.time()
                return

            exclude = ['ruby', 'yubi', 'philippines', 'karlo', 'himari', 'megumi', 'angelo']
            exclude_himari = ['himari']
            exclude_megumi = ['megumi']

        message_content = message.content.lower()

        if any(re.search(r'\b' + re.escape(word) + r'\b', message_content) for word in exclude):
                return

        iyot_mentioned = ['iyot', 'eut', 'iot', 'iyut', 'sex', 'cex', 'seks', 'secks', 'cecks', 'ceks', 'kantot', 'kantotan', 'kantut', 'kantutan', 'sisig express', 'kanton', 'kantonan', 'kantunan', 'canton', 'seggs', 'segg', 'segs', 'eot', 'eyot', 'eyut']
        if any(word in message.content.lower() for word in iyot_mentioned):
                await message.channel.send('iyot mentioned')
                cooldowns[message.author.id] = time.time()
                return
            
        ub_mentioned = ['m4h1ru', 'mahiru', 'mahiruu', 'mah1ru', 'm4hiru', 'mr m', 'redacted', 'delulu', 'kral', 'karl', 'karl angelo reyes', 'karl reyes', 'philip', 'ayaka', 'mr p', 'm4h1ruu', 'mah1ruu', 'm4hiruu', 'kr4l', 'k4rl', 'ugly bastard', ':ub:', 'lil bro', 'nui', 'mr n', 'mr b', 'bernard', 'tungsten', 'tungstendeagle', 'tungstenfuckface', 'fuckface', 'kristian', 'kalansay', 'gelo', 'moraleja', 'gelo moraleja']
        if any(word in message.content.lower() for word in ub_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('<:ub:1178729920730509372>')
                    cooldowns[message.author.id] = time.time()
                    return
                    
        mika_mentioned = ['mika', 'MikaXD', 'XD', 'gorilla', 'xd', 'ayaya', '🦍']
        if any(word in message.content.lower() for word in mika_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):    
                    await message.channel.send('<:MikaXD:1179436633779613696>')
                    cooldowns[message.author.id] = time.time()
                    return
            
        posa_mentioned = ['pusa', 'posa', 'cat', 'pussy', 'kuting']
        if any(word in message.content.lower() for word in posa_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('posa <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
            
        miaw_mentioned = ['miaw', 'meow', 'nyan']
        if any(word in message.content.lower() for word in miaw_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('<:miaw:1179606920693305467>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        elf_mentioned = ['elysia', 'iori', 'frieren', 'nanagami rin', 'junko', 'chinatsu', 'ayane', 'muelsyse', 'mumu', 'aomori mine', 'megu', 'himari', 'preyren', 'layla', 'oki aoi']
        if any(word in message.content.lower() for word in elf_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    if not any(re.search(rf'\b{word}\b', message.content.lower()) for word in exclude_megumi):
                        with open(r'C:\gian_bot\images\iyot.png', 'rb') as y:
                            picture2 = discord.File(y)
                            await message.channel.send(file=picture2)
                            cooldowns[message.author.id] = time.time()
                            return

        posa_char_mentioned = ['kazusa', 'kikyou', 'serika', 'mari', 'momoi', 'midori', 'akira', 'kirara', 'diona', 'lynette', 'rosmontis']
        if any(word in message.content.lower() for word in posa_char_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    if not any(re.search(rf'<:\w*:{word}>', message.content) for word in exclude_himari):
                        await message.channel.send('posa <:bocchi_ehehe:1179447995931049984>')
                        cooldowns[message.author.id] = time.time()
                        return
                    
        alya_char_mentioned = ['alya', 'alisa', 'mikhailovna']
        if any(word in message.content.lower() for word in alya_char_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('alya <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        pekeng_posa_char_mentioned = ['shiroko']
        if any(word in message.content.lower() for word in pekeng_posa_char_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('pekeng posa <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        rumi_mentioned = ['rumi']
        if any(word in message.content.lower() for word in rumi_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('rumi <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        ichika_mentioned = ['ichika']
        if any(word in message.content.lower() for word in ichika_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('ichika <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        baubau_mentioned = ['baubau', 'bau bau', 'fuwamoco', 'fuwawa', 'mococo', 'hibiki', 'ceobe']
        if any(word in message.content.lower() for word in baubau_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('baubau <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        korone_mentioned = ['korone', 'yubi', 'koone']
        if any(word in message.content.lower() for word in korone_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('yubi yubi <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        ruby_mentioned = ['ruby']
        if any(word in message.content.lower() for word in ruby_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('ruby <:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        daga_mentioned = ['daga', 'rat', 'rrat']
        if any(word in message.content.lower() for word in daga_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('🖕🐀')
                    cooldowns[message.author.id] = time.time()
                    return
                
        topaz_mentioned = ['topaz']
        if any(word in message.content.lower() for word in topaz_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('🍑 just tell everyone on our team 🍑')
                    cooldowns[message.author.id] = time.time()
                    return
                
        ogey_mentioned = ['ogey', 'ogei']
        if any(word in message.content.lower() for word in ogey_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('rrat')
                    cooldowns[message.author.id] = time.time()
                    return
                
        tikoy_mentioned = ['loli', 'uo', 'uoh', 'cunny', 'cnuuy', 'cnnuy', 'kani', '😭', '🦀']
        if any(word in message.content.lower() for word in tikoy_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('😭')
                    cooldowns[message.author.id] = time.time()
                    return
                
        bocchi_mentioned = ['bocchi', 'hitori goto', 'hitori gotoh', 'hitori gotou', 'bocc', 'bocchers', 'hitori', 'gotoh', 'gotou']
        if any(word in message.content.lower() for word in bocchi_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('<:bocchi_ehehe:1179447995931049984>')
                    cooldowns[message.author.id] = time.time()
                    return
                
        sadhamster_mentioned = [':sadhamster:']
        if any(word in message.content.lower() for word in sadhamster_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    await message.channel.send('<:sadhamster:1211275120375496734>')
                    cooldowns[message.author.id] = time.time()
                    return
                
            # tite_mentioned = ['tite', 'oten']
            # if any(word in message.content.lower() for word in tite_mentioned):
            #     if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
            #         if message.channel.id == 1175265248559767574: 
            #             await message.channel.send('Wala non si tikoy <:Ping:1199608960412565594>')
            #             cooldowns[message.author.id] = time.time()
            #             return
                
            # ga_mentioned = ['ga']
            # if any(word in message.content.lower() for word in ga_mentioned):
            #     if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
            #         await message.channel.send('ga mentioned <:bocchi_ehehe:1179447995931049984>')

        if message.stickers:
                for sticker in message.stickers:
                    if sticker.name == "niggasaki":
                        await message.channel.send(sticker.url)
                        cooldowns[message.author.id] = time.time()
                        return
                
        if message.stickers:
                for sticker in message.stickers:
                    if sticker.name == "MIAW":
                        await message.channel.send(sticker.url)
                        cooldowns[message.author.id] = time.time()
                        return
                
                # if message.stickers:
                #     for sticker in message.stickers:
                #         if sticker.name == "iyot":
                #             await message.channel.send(sticker.url)

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
                    with open(r'C:\gian_bot\images\Ruby_Bonk.gif', 'rb') as ruby:
                        pictureRuby = discord.File(ruby)
                        await message.channel.send(file=pictureRuby)
                    # for reaction in reactions:
                    #     await message.add_reaction(reaction)
                        await client.change_presence(activity=discord.Game(name=f"Appreciated {count_data['goodBotCount']} times and abused {abuse_data['badBotCount']} times"))
                        cooldowns[message.author.id] = time.time()
                
        with open('bad_bot_counter.json', 'w') as file:
                json.dump({'badBotCount': abuse_data['badBotCount']}, file)

            # yuuka_sticker_id = 1186217513114140754
        yuuka_mentioned = ['yuuka']
        if any(word in message.content.lower() for word in yuuka_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\yuuka.png', 'rb') as x:
                        picture = discord.File(x)
                        await message.channel.send(file=picture)
                        cooldowns[message.author.id] = time.time()
                        
        jarvis_mentioned = ['jarvis', 'jabol', 'jakol']
        if any(word in message.content.lower() for word in jarvis_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\jarvis.png', 'rb') as x:
                        picture = discord.File(x)
                        await message.channel.send(file=picture)
                        cooldowns[message.author.id] = time.time()
                        
        kys_mentioned = ['i want to die', 'i want to kill myself', 'i want to kms', 'i wanna kms', 'i wanna kill myself', 'kys', 'keep yourself safe']
        if any(word in message.content.lower() for word in kys_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\dont_kys.mp4', 'rb') as video:
                        video_file = discord.File(video)
                        await message.channel.send(file=video_file)
                        cooldowns[message.author.id] = time.time()
                        
        nigga_mentioned = ['nigga', 'nigger', 'nibba']
        if any(word in message.content.lower() for word in nigga_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\nigger.png', 'rb') as x:
                        picture = discord.File(x)
                        await message.channel.send(file=picture)
                        cooldowns[message.author.id] = time.time()                
                
        menhera_mentioned = ['menhera']
        if any(word in message.content.lower() for word in menhera_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\MikaSurprised.png', 'rb') as mika:
                        picture = discord.File(mika)
                        await message.channel.send(file=picture)
                        cooldowns[message.author.id] = time.time()
                
        gojo_mentioned = ['gojo']
        if any(word in message.content.lower() for word in gojo_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\gojo_reaction.gif', 'rb') as gojo:
                        pictureGojo = discord.File(gojo)
                        await message.channel.send(file=pictureGojo)
                
        byakuya_mentioned = ['byakuya']
        if any(word in message.content.lower() for word in byakuya_mentioned):
                if not re.match(r'^https?:\/\/.*[\r\n]*', message.content):
                    with open(r'C:\gian_bot\images\byakuya.jpg', 'rb') as z:
                        picture3 = discord.File(z)
                        await message.channel.send(file=picture3)
                        cooldowns[message.author.id] = time.time()
                        return
                

            # if message.content == 'sticker get id':
            #     sticker_name = 'iyot'  # Replace with the name of the sticker
            #     sticker = discord.utils.get(message.guild.stickers, name=sticker_name)
            #     if sticker:
            #         await message.channel.send(f"The ID of the sticker {sticker_name} is {sticker.id}")
            #     else:
            #         await message.channel.send(f"The sticker {sticker_name} was not found")

client.run('MTE3NTc5OTgyNjI4NjM3OTE4Mw.GErLtx.Vt-Hr5j1CvrIE5AsS6M-Ytmq3PrUoz29roHwdg')