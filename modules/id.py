async def id(_,message):
    await message.reply_text(
        f"Chat ID = `{message.chat.id}`\n"
        f"Message ID = `{message.message_id}`\n"
        f"Replied User ID = `{message.reply_to_message.from_user.id if message.reply_to_message is not None else None}`\n",
        
        quote=True)