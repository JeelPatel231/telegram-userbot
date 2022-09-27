from pyrogram import Client

api_id = int(input("Enter API ID : "))

api_hash = str(input("Enter API HASH : "))

app = Client(name=None,in_memory=True,api_id=api_id,api_hash=api_hash)

with app:
    sess_str = app.export_session_string()
    app.send_message("me",sess_str)
    print("--------------")
    print(sess_str)
    print("--------------")
    print("this is also sent to your saved messages")