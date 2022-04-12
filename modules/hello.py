async def hello(client,message):
    await message.reply_text("hello", quote=True)