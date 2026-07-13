# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import json
import sys
import threading
import asyncio 
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE, LOGIN_SYSTEM, STRING_SESSION, CHANNEL_ID, WAITING_TIME
from database.db import db
from TechVJ.strings import HELP_TXT
from bot import TechVJUser

# Stdin listener to skip current message by typing 'q'
def terminal_input_listener():
    while True:
        try:
            line = sys.stdin.readline()
            if 'q' in line.lower():
                print("\n[Input] 'q' detected. Skipping current message...")
                batch_temp.SKIP_CURRENT = True
        except Exception:
            pass

threading.Thread(target=terminal_input_listener, daemon=True).start()

# ── Resume State Helpers ──────────────────────────────────────────────────────
RESUME_FILE = "database/resume_state.json"

def save_resume_state(user_id: int, url: str, current_msgid: int, to_id: int):
    """Persist the current batch progress so it can be resumed after a crash."""
    try:
        data = {}
        if os.path.exists(RESUME_FILE):
            with open(RESUME_FILE, "r") as f:
                data = json.load(f)
        data[str(user_id)] = {"url": url, "current_msgid": current_msgid, "to_id": to_id}
        with open(RESUME_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

def load_resume_state(user_id: int):
    """Load any saved batch state for the user. Returns dict or None."""
    try:
        if os.path.exists(RESUME_FILE):
            with open(RESUME_FILE, "r") as f:
                data = json.load(f)
            return data.get(str(user_id))
    except Exception:
        pass
    return None

def clear_resume_state(user_id: int):
    """Clear saved state once a batch finishes successfully."""
    try:
        if os.path.exists(RESUME_FILE):
            with open(RESUME_FILE, "r") as f:
                data = json.load(f)
            data.pop(str(user_id), None)
            with open(RESUME_FILE, "w") as f:
                json.dump(data, f, indent=4)
    except Exception:
        pass
# ─────────────────────────────────────────────────────────────────────────────

class batch_temp(object):
    IS_BATCH = {}
    SKIP_CURRENT = False

async def downstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Downloaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# upload status
async def upstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Uploaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# progress writer
def progress(current, total, message, type):
    if getattr(batch_temp, 'SKIP_CURRENT', False):
        raise Exception("Skipped by user")
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        current_mb = current / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        fileup.write(f"{current * 100 / total:.1f}% ({current_mb:.1f}MB / {total_mb:.1f}MB)")


# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url = "https://t.me/kingvj01")
    ],[
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/vj_bots')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\nFor downloading restricted content /login first.\n\nKnow how to use bot by - /help</b>", 
        reply_markup=reply_markup, 
        reply_to_message_id=message.id
    )
    return


# help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"{HELP_TXT}"
    )

# cancel command
@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    clear_resume_state(message.from_user.id)
    await client.send_message(
        chat_id=message.chat.id, 
        text="**Batch Successfully Cancelled.**"
    )

# resume command
@Client.on_message(filters.command(["resume"]))
async def send_resume(client: Client, message: Message):
    state = load_resume_state(message.from_user.id)
    if state is None:
        return await message.reply("**No pending batch found to resume.**")
    await message.reply(
        f"**Resuming batch from Msg ID `{state['current_msgid']}` to `{state['to_id']}`...**\n"
        f"Send the same link again starting from ID `{state['current_msgid']}` to resume.\n\n"
        f"Or just resend:**\n`{state['url']}`**"
    )

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    # Joining chat
    if ("https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text) and LOGIN_SYSTEM == False:
        if TechVJUser is None:
            await client.send_message(message.chat.id, "String Session is not Set", reply_to_message_id=message.id)
            return
        try:
            try:
                await TechVJUser.join_chat(message.text)
            except Exception as e: 
                await client.send_message(message.chat.id, f"Error : {e}", reply_to_message_id=message.id)
                return
            await client.send_message(message.chat.id, "Chat Joined", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await client.send_message(message.chat.id, "Chat already Joined", reply_to_message_id=message.id)
        except InviteHashExpired:
            await client.send_message(message.chat.id, "Invalid Link", reply_to_message_id=message.id)
        return
    
    if "https://t.me/" in message.text:
        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            return await message.reply_text("**One Task Is Already Processing. Wait For Complete It. If You Want To Cancel This Task Then Use - /cancel**")
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        if LOGIN_SYSTEM == True:
            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply("**For Downloading Restricted Content You Have To /login First.**")
                return
            api_id = int(await db.get_api_id(message.from_user.id))
            api_hash = await db.get_api_hash(message.from_user.id)
            try:
                acc = Client("saverestricted", session_string=user_data, api_hash=api_hash, api_id=api_id)
                await acc.connect()
            except:
                return await message.reply("**Your Login Session Expired. So /logout First Then Login Again By - /login**")
        else:
            if TechVJUser is None:
                await client.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                return
            acc = TechVJUser
				
        batch_temp.IS_BATCH[message.from_user.id] = False
        should_break = False
        for msgid in range(fromID, toID+1):
            if batch_temp.IS_BATCH.get(message.from_user.id): break

            # Save resume state before processing each message
            save_resume_state(message.from_user.id, message.text, msgid, toID)
            print(f"[Processing] User: {message.from_user.id} | Msg ID: {msgid} / {toID}")

            # Process the message with retries on network error, and infinite retry on FloodWait
            attempt = 1
            while attempt <= 3:
                if batch_temp.IS_BATCH.get(message.from_user.id):
                    should_break = True
                    break
                try:
                    # private
                    if "https://t.me/c/" in message.text:
                        chatid = int("-100" + datas[4])
                        await handle_private(client, acc, message, chatid, msgid)

                    # bot
                    elif "https://t.me/b/" in message.text:
                        username = datas[4]
                        await handle_private(client, acc, message, username, msgid)

                    # public
                    else:
                        username = datas[3]
                        try:
                            msg = await client.get_messages(username, msgid)
                        except UsernameNotOccupied:
                            await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                            should_break = True
                            break
                        try:
                            await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                        except:
                            await handle_private(client, acc, message, username, msgid)
                    break  # Success — exit retry loop

                except FloodWait as fw:
                    print(f"[FloodWait] Sleeping {fw.value}s on msg {msgid}")
                    if ERROR_MESSAGE:
                        await client.send_message(message.chat.id, f"⏳ Rate limit reached (FloodWait). Sleeping for {fw.value}s before retrying Msg ID `{msgid}`...", reply_to_message_id=message.id)
                    await asyncio.sleep(fw.value)
                    # Note: Do not increment attempt count, retry immediately
                    continue
                except (OSError, asyncio.TimeoutError, ConnectionError) as e:
                    wait = attempt * 5
                    print(f"[NetworkError] Attempt {attempt}/3 on msg {msgid}: {e}. Retrying in {wait}s...")
                    if attempt == 3:
                        if ERROR_MESSAGE:
                            await client.send_message(message.chat.id, f"⚠️ Network error on msg `{msgid}` after 3 retries: `{e}`.\nBatch paused. Use /resume to continue.", reply_to_message_id=message.id)
                        should_break = True
                        break
                    else:
                        await asyncio.sleep(wait)
                        attempt += 1
                except Exception as e:
                    if str(e) == "Skipped by user":
                        print(f"[Skipped] Msg ID: {msgid} by user request")
                        batch_temp.SKIP_CURRENT = False
                        break
                    if ERROR_MESSAGE:
                        await client.send_message(message.chat.id, f"❌ Error on msg `{msgid}`: `{e}`.\nBatch paused. Use /resume to continue.", reply_to_message_id=message.id)
                    should_break = True
                    break
            
            if should_break:
                break

            # wait time
            await asyncio.sleep(WAITING_TIME)
        if LOGIN_SYSTEM == True:
            try:
                await acc.disconnect()
            except:
                pass
        batch_temp.IS_BATCH[message.from_user.id] = True
        if not should_break:
            clear_resume_state(message.from_user.id)  # Batch done — clear saved state
            print(f"[Done] User: {message.from_user.id} | Batch completed up to msg {toID}")
        else:
            print(f"[Paused] User: {message.from_user.id} | Batch paused at msg {msgid}")


def get_file_size(msg: Message):
    try:
        if msg.document: return msg.document.file_size
    except: pass
    try:
        if msg.video: return msg.video.file_size
    except: pass
    try:
        if msg.audio: return msg.audio.file_size
    except: pass
    try:
        if msg.photo: return msg.photo.file_size
    except: pass
    try:
        if msg.voice: return msg.voice.file_size
    except: pass
    try:
        if msg.animation: return msg.animation.file_size
    except: pass
    try:
        if msg.sticker: return msg.sticker.file_size
    except: pass
    return None

# handle private
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    if msg.empty: return 
    msg_type = get_message_type(msg)
    if not msg_type: return 

    size = get_file_size(msg)
    if size:
        size_mb = size / (1024 * 1024)
        print(f"[Downloading] Msg ID: {msgid} | Type: {msg_type} | Size: {size_mb:.1f} MB")
    else:
        print(f"[Downloading] Msg ID: {msgid} | Type: {msg_type}")

    if CHANNEL_ID:
        try:
            chat = int(CHANNEL_ID)
        except:
            chat = message.chat.id
    else:
        chat = message.chat.id
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
    if "Text" == msg_type:
        if not msg.text or not msg.text.strip():
            return  # Skip empty text messages to avoid MESSAGE_EMPTY error
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return 
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return  

    smsg = await client.send_message(message.chat.id, '**Downloading**', reply_to_message_id=message.id)
    asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, chat))
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message,"down"])
        os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        if str(e) == "Skipped by user":
            raise e
        if ERROR_MESSAGE == True:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML) 
        return await smsg.delete()
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
    asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, chat))

    if msg.caption:
        caption = msg.caption
    else:
        caption = None
    if batch_temp.IS_BATCH.get(message.from_user.id): return 
            
    if "Document" == msg_type:
        try:
            ph_path = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_document(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        if ph_path != None: os.remove(ph_path)
        

    elif "Video" == msg_type:
        try:
            ph_path = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_video(chat, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        if ph_path != None: os.remove(ph_path)

    elif "Animation" == msg_type:
        try:
            await client.send_animation(chat, file, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        
    elif "Sticker" == msg_type:
        try:
            await client.send_sticker(chat, file, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)     

    elif "Voice" == msg_type:
        try:
            await client.send_voice(chat, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)

    elif "Audio" == msg_type:
        try:
            ph_path = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            ph_path = None

        try:
            await client.send_audio(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML, progress=progress, progress_args=[message,"up"])   
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        
        if ph_path != None: os.remove(ph_path)

    elif "Photo" == msg_type:
        try:
            await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            if str(e) == "Skipped by user":
                raise e
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
    
    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
    if file and os.path.exists(file):
        os.remove(file)
    await client.delete_messages(message.chat.id,[smsg.id])


# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass
        

# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
