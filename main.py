from config import Config
from bot.client import BotClient
import logging

def main():
    try:
        config = Config()
        client = BotClient(config)
        client.run(config.TOKEN)
    except Exception as e:
        logging.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()