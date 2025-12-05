


*A Telegram Bot, Which Can Send You Restricted Content By It's Post Link With <b>Login Feature.</b>*

*Added **TG Account Protection** Security To Prevent Account From Ban Issue, Not Totally But Now TG Account Ban Chance Is Low.*

---

<b>Watch Video Tutorial - [Click Here](https://youtu.be/BFEvSX5vIMg)</b>

---

## Setup for Local Deployment

Follow these steps to set up and run the bot locally on your machine.

### Prerequisites

*   Python 3.x installed
*   `pip` (Python package installer)

### 1. Virtual Environment Setup

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

With your virtual environment activated, install all required Python packages:

```bash
pip install -r requirements.txt
```
  1 python3 -m venv .venv
   2 source .venv/bin/activate
   3 pip install -r requirements.txt
   4 chmod +x start_local.sh
   5 ./start_local.sh


### 3. Configure Environment Variables

The bot uses environment variables for configuration. Create a `.env` file in the root directory of the project and populate it with your credentials.

```bash
# Example .env file content (create this file if it doesn't exist)
# nano .env
# ---------------------------------------------------------------
API_ID=YOUR_API_ID                        # Get from my.telegram.org
API_HASH=YOUR_API_HASH                    # Get from my.telegram.org
BOT_TOKEN=YOUR_BOT_TOKEN                  # Get from @BotFather
ADMINS=YOUR_ADMIN_USER_ID                 # Your numeric Telegram User ID
LOGIN_SYSTEM=True                         # Set True or False as per your need (default is True)
# STRING_SESSION="YOUR_SESSION_STRING_HERE" # Required if LOGIN_SYSTEM is False. Uncomment and set.
# CHANNEL_ID=-1001234567890               # Optional: Your channel ID (bot must be admin)
# WAITING_TIME=10                           # Optional: Increase time to avoid floodwait (default is 10 seconds)
# ERROR_MESSAGE=True                        # Optional: Set True/False for error messages (default is True)
# ---------------------------------------------------------------
```
**Note:** `DB_URI` is no longer required as the bot now uses a local JSON file (`database/users.json`) for data storage, eliminating the need for MongoDB.

### 4. Running the Bot

Once the setup is complete, you can run the bot using the provided script:

```bash
# Ensure the script is executable
chmod +x start_local.sh

# Run the bot
./start_local.sh
```
This script will start the bot, and it will use the local JSON database `database/users.json` to store user sessions and other data.

---

## Bot Variables

These are the variables the bot uses, now loaded from your `.env` file:

-   `LOGIN_SYSTEM`: Set `True` or `False` based on whether you want the in-bot login feature.
-   `STRING_SESSION`: Your Pyrogram session string. Required if `LOGIN_SYSTEM` is `False`.
-   `API_HASH`: Your API Hash from [my.telegram.org](https://my.telegram.org).
-   `API_ID`: Your API ID from [my.telegram.org](https://my.telegram.org).
-   `BOT_TOKEN`: Your Bot Token from [@BotFather](https://telegram.me/BotFather).
-   `ADMINS`: Your Admin User ID for broadcasting messages.
-   `CHANNEL_ID`: Your Channel ID on which the bot uploads content. The bot must be an admin with full rights. Leave blank if not needed.
-   `WAITING_TIME`: Time (in seconds) to wait between processing messages to avoid spamming and Telegram account bans.
-   `ERROR_MESSAGE`: Set `True` or `False`. If `True`, error messages will be sent to the user.

---

## Commands

-   `/start`: Check if the bot is working.
-   `/help`: Get information on how to use the bot.
-   `/login`: Log in your Telegram String Session via the bot.
-   `/logout`: Log out your current session.
-   `/cancel`: Cancel any ongoing task.
-   `/broadcast`: Broadcast a message to all users (Admin Only).

---

## Usage

**FOR PUBLIC CHATS**

_Just send the post/s link._


**FOR PRIVATE CHATS**

_First, send the invite link of the chat (unnecessary if the account of the string session is already a member of the chat), then send the post/s link._


**FOR BOT CHATS**

_Send a link with '/b/', bot's username, and message ID. You might want to install some unofficial client (like Plus Messenger) to get the ID like below:_

```
https://t.me/b/botusername/4321
```

**MULTI POSTS**

_Send public/private posts links as explained above with the format "from - to" to send multiple messages like below:_

```
https://t.me/xxxx/1001-1010

https://t.me/c/xxxx/101 - 120
```

_Note that spaces in between don't matter._

---

## Credits

-   <b>Thanks To [BipinKrish](https://github.com/bipinkrish) For Base Repo
-   Thanks To [Tech VJ](https://github.com/VJBots) For Modification.</b>
