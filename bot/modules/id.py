from pyrogram.handlers.message_handler import MessageHandler
from bot import app, on_cmd
from bot.UBModule import UBModule


def id_handler(_, message):
    message.reply_text(
        f"Chat ID = `{message.chat.id}`\n"
        f"Message ID = `{message.id}`\n"
        f"Replied User ID = `{message.reply_to_message.from_user.id if message.reply_to_message is not None else None}`\n",
        quote=True,
    )


id_module = UBModule(
    name="id",
    help_text="id help text",
    handler=MessageHandler(id_handler, on_cmd("id")),
)

app.register_module(id_module)
