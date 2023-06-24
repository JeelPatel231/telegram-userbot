from pyrogram.handlers.message_handler import MessageHandler
from bot import app, on_cmd
from datetime import datetime
from bot.UBModule import UBModule


async def ping_handler(client, mess):
    start = datetime.now()
    ping_mess = await client.send_message("me", "ping test")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await mess.reply_text(f"`Pong!\n{duration}ms`", quote=True)
    await ping_mess.delete()


app.register_module(
    UBModule(
        name="ping",
        help_text="ping help text",
        handler=MessageHandler(ping_handler, on_cmd("ping")),
    )
)
