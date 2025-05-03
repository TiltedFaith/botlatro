def setup_handlers(client):
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        print(f"Received message: {message.content}")
        
        if message.content.lower() == 'ye':
            print("Triggered 'ye' response")
            await message.channel.send('ye')