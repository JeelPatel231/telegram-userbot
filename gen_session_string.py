from pyrogram import Client
from dotenv import dotenv_values

config = dotenv_values(".env")

try:
    api_id = config["API_ID"]
except KeyError:
    api_id = int(input("Enter API ID : "))

try:
    api_hash = config["API_HASH"]
except KeyError:
    api_hash = str(input("Enter API HASH : "))

app = Client("bruh",api_id=api_id,api_hash=api_hash,in_memory=True)

with app:
    sess_str = app.export_session_string()
    app.send_message("me",sess_str)
    print("--------------")
    print(sess_str)
    print("--------------")
    print("this is also sent to your saved messages")
