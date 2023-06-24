from threading import Thread
from pyrogram import filters, types
from dotenv import dotenv_values
import os
import logging
from bot.UBModule import UBModule
from typing import Optional, Union
from io import BytesIO
from pyrogram.client import Client


config = {
    **dotenv_values(),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

blacklisted_chats = []
COMMAND_PREFIX = config.get("COMMAND_PREFIX", ".")

logging.basicConfig(level=logging.INFO)


def run_threaded(fn):
    def x(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()

    return x


def on_cmd(data: str):
    async def func(flt, _, message: types.Message):
        return (
            message.outgoing
            and str(message.chat.id) not in blacklisted_chats
            and message.text is not None
            and message.from_user is not None
            and message.text.split()[0] == f"{COMMAND_PREFIX}{flt.data}"
        )

    return filters.create(func, data=data)


class UBClient(Client):
    def register_module(self, module: UBModule):
        self.add_handler(module.handler)

    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        reply_to_message_id: Optional[int] = None,
        *args,
        **kwargs,
    ) -> Optional[types.Message]:
        if len(text) <= 4096:
            return await super().send_message(chat_id, text, *args, **kwargs)

        stream = BytesIO(text.encode())
        stream.name = "output.txt"

        return await super().send_document(
            chat_id, stream, reply_to_message_id=reply_to_message_id
        )


app = UBClient(
    name="nice name",
    session_string=config["SESSION_STRING"],
    api_id=config["API_ID"],
    api_hash=config["API_HASH"],
)
