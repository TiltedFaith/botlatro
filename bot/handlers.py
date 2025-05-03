import os
import discord
from pathlib import Path

def setup_handlers(client):
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        print(f"Received message: {message.content}")
        
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

        '''
        # YE RESPONSE
        if message.content.lower() == 'ye':
            print("Triggered 'ye' response")
            await message.channel.send('ye')
        '''

        
        