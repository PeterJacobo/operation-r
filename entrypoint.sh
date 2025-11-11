#!/bin/bash

# Authenticate ngrok
ngrok config add-authtoken "$NGROK_AUTHTOKEN"

# Start ngrok in the background
ngrok http 5000 --log=stdout > /tmp/ngrok.log 2>&1 &

echo "ngrok started in background"
echo "Starting email fetcher..."

# Check for required files
if [ ! -f "credentials.json" ]; then
    echo "ERROR: credentials.json not found!"
    exit 1
fi

if [ ! -f "token.pickle" ]; then
    echo "ERROR: token.pickle not found!"
    exit 1
fi

echo "All required files present"

# Run email fetcher (this runs in a loop, so it won't exit)
echo "Running python3 fetch_emails.py..."
python3 fetch_emails.py 2>&1

echo "fetch_emails.py exited unexpectedly"
tail -f /dev/null

# Start your Flask app (won't be reached unless fetch_emails.py exits)
# python3 main.py