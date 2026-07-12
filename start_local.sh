#!/bin/bash

echo "Starting VJ Save Restricted Bot Locally..."
echo "Using local JSON database (database/users.json)"

# Ensure the database directory exists
mkdir -p database

# =========================================================================
# Environment Variable Setup:
# It's recommended to set your environment variables in a `.env` file
# in the project root directory.
#
# Example `.env` file content:
# API_ID=1234567
# API_HASH=abcdef1234567890abcdef1234567890
# BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
# ADMINS=1234567890
# LOGIN_SYSTEM=True
# # STRING_SESSION="YOUR_SESSION_STRING_HERE" # Uncomment and set if LOGIN_SYSTEM is False
# CHANNEL_ID=-1001234567890 # Optional: Your channel ID
# WAITING_TIME=10
# ERROR_MESSAGE=True
#
# Alternatively, you can export them directly in your terminal before running:
# export API_ID="1234567"
# export API_HASH="abcdef1234567890abcdef1234567890"
# export BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
# export ADMINS="1234567890"
# export LOGIN_SYSTEM="True"
# # export STRING_SESSION="YOUR_SESSION_STRING_HERE"
# export CHANNEL_ID="-1001234567890"
# export WAITING_TIME="10"
# export ERROR_MESSAGE="True"
#
# Note: DB_URI is no longer needed as the bot now uses a local JSON file.
# =========================================================================

# Activating virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "Activating virtual environment (venv)..."
    source venv/bin/activate
fi

# Gracefully handle Ctrl+C / SIGINT and SIGTERM
trap "echo -e '\nStopping bot gracefully...'; exit 0" SIGINT SIGTERM

# Run the bot
python3 -u bot.py