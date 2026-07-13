# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import os
import glob

# Clean up leftover progress files from previous runs
for f in glob.glob("*status.txt"):
    try:
        os.remove(f)
    except:
        pass

import asyncio
import signal
import sys
import logging

# Silence Pyrogram reconnect warnings/info spam
logging.getLogger("pyrogram").setLevel(logging.ERROR)

def signal_handler(sig, frame):
    print('\nStopping bot and exiting immediately...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, LOGIN_SYSTEM

if STRING_SESSION is not None and LOGIN_SYSTEM == False:
	TechVJUser = Client("TechVJ", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
	TechVJUser.start()
else:
    TechVJUser = None

class Bot(Client):

    def __init__(self):
        super().__init__(
            "techvj login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=150,
            sleep_threshold=5
        )

      
    async def start(self):
            
        await super().start()
        print('Bot Started Powered By @VJ_Bots')

    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

if __name__ == "__main__":
    bot = Bot()
    bot.run()

# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01