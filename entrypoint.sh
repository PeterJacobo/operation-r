#!/bin/bash
set -e

# Authenticate ngrok
ngrok config add-authtoken "$NGROK_AUTHTOKEN"

# Start ngrok in the background
ngrok http 5000 --log=stdout &

# Run email fetcher
python3 fetch_emails.py

# Start your Flask app
# python3 main.py