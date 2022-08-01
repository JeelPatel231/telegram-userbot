from bot import app, on_cmd

@app.on_message(filters=on_cmd("id"))
def _(_,message):
    message.reply_text(
        f"Chat ID = `{message.chat.id}`\n"
        f"Message ID = `{message.id}`\n"
        f"Replied User ID = `{message.reply_to_message.from_user.id if message.reply_to_message is not None else None}`\n",
        quote=True)

@app.on_message(filters=on_cmd("help id"))
def _(_,m):
    m.reply_text("`Shows ID of chat,message and user`")