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

# Ensure event loop is created and set before importing any Pyrogram module
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import signal
import sys
import logging

# Silence Pyrogram reconnect warnings/info spam
logging.getLogger("pyrogram").setLevel(logging.ERROR)



# Register SIGINT (Ctrl+C) and SIGTERM at Python VM level — os._exit bypasses all asyncio/Pyrogram shutdown hooks
def _force_exit(sig, frame):
    print('\nStopping bot immediately...')
    os._exit(0)

signal.signal(signal.SIGINT, _force_exit)
signal.signal(signal.SIGTERM, _force_exit)



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
    async def main():
        bot = Bot()
        try:
            await bot.start()
            await asyncio.Event().wait()  # Run forever until interrupted
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            try:
                await bot.stop()
            except Exception:
                pass
            os._exit(0)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        os._exit(0)

# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01