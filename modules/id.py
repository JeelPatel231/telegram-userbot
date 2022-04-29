def id(_,message):
    message.reply_text(
        f"Chat ID = `{message.chat.id}`\n"
        f"Message ID = `{message.message_id}`\n"
        f"Replied User ID = `{message.reply_to_message.from_user.id if message.reply_to_message is not None else None}`\n",
        
        quote=True)

help = "`Shows ID of chat,message and user`"