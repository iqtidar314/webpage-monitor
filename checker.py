import requests
import hashlib
import os

# URL to monitor
URL = "https://dhakacollege.edu.bd/notice"
HASH_FILE = "hash.txt"

# Telegram settings
BOT_TOKEN = os.getenv("8110801820:AAFZo_fkG0VPunmc2ErG4Hwejn8YaNcQMRs
")
CHAT_ID = os.getenv("5076910986")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Fetch the webpage content
response = requests.get(URL)
content = response.text

# Compute hash of the page content
new_hash = hashlib.md5(content.encode()).hexdigest()

# Load the old hash (if exists)
old_hash = None
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as file:
        old_hash = file.read()

# Compare hashes and send Telegram notification if changed
if old_hash != new_hash:
    message = f"🚨 The notice page has been updated! Check it here: {URL}"
    requests.get(TELEGRAM_API, params={"chat_id": CHAT_ID, "text": message})

    # Save new hash
    with open(HASH_FILE, "w") as file:
        file.write(new_hash)
