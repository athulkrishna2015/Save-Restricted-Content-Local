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

# Monkey-patch Pyrogram TCP transport to prevent AttributeError in recv() on disconnect
try:
    import pyrogram.connection.transport.tcp.tcp as pyrogram_tcp
    original_recv = pyrogram_tcp.TCP.recv
    async def patched_recv(self, length: int = 0):
        if self.reader is None:
            return None
        try:
            return await original_recv(self, length)
        except AttributeError:
            return None
    pyrogram_tcp.TCP.recv = patched_recv
except Exception as e:
    logging.error(f"Failed to monkey-patch Pyrogram TCP transport: {e}")

def _force_exit(sig_name):
    print(f'\nReceived {sig_name}. Stopping bot immediately...')
    os._exit(0)

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
    import platform

    async def main():
        loop = asyncio.get_running_loop()

        # Register SIGINT (Ctrl+C) and SIGTERM using the async-safe loop handler
        if platform.system() != "Windows":
            loop.add_signal_handler(signal.SIGINT, _force_exit, "SIGINT")
            loop.add_signal_handler(signal.SIGTERM, _force_exit, "SIGTERM")

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