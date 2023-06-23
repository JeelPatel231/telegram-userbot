from pyrogram.client import Client
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message
from bot import app, on_cmd

@app.on_message(filters=on_cmd("load"))
async def _(client: Client,message: Message):
    
    if message.reply_to_message is None or \
        message.reply_to_message.media != MessageMediaType.DOCUMENT or \
        not message.reply_to_message.document.file_name.endswith(".py"):

        return await message.reply_text("Reply to a document, with `.py` ext")

    downloaded_doc = await client.download_media(
            message.reply_to_message, 
            in_memory=True
        )

    if downloaded_doc is None:
        return await message.reply_text("document was none")

    if isinstance(downloaded_doc, str):
        return await message.reply_text("document was of type string, aborting")
    downloaded_doc.seek(0)
    
    exec(downloaded_doc.read(), {})

    await message.reply_text("Mod Loaded Successfully!")
