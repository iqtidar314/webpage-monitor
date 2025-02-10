import os
import requests
from bs4 import BeautifulSoup
import hashlib

TELEGRAM_API = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"
URL = "https://dhakacollege.edu.bd/notice"
FILE_PATH = ".github/scripts/previous_content.html"

def get_content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def send_notification(message):
    data = {
        "chat_id": os.environ['CHAT_ID'],
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(TELEGRAM_API, data=data)

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
clean_content = soup.prettify()
current_hash = get_content_hash(clean_content)

try:
    with open(FILE_PATH, 'r') as f:
        previous_hash = get_content_hash(f.read())
except FileNotFoundError:
    previous_hash = ""

if current_hash != previous_hash:
    message = f"🚨 <b>Website Changed!</b> 🚨\n\n🔗 {URL}"
    send_notification(message)
    with open(FILE_PATH, 'w') as f:
        f.write(clean_content)
    print("Change detected! Notification sent.")
else:
    print("No changes detected.")
