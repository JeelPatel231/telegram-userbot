from threading import Thread
from pyrogram import Client, filters
from dotenv import dotenv_values
import os
import logging

config = {
    **dotenv_values(),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

blacklisted_chats = []
COMMAND_PREFIX = config.get("COMMAND_PREFIX",".")

logging.basicConfig(level=logging.INFO)

def run_threaded(fn):
    def x(*args, **kwargs):
        Thread(target=fn,args=args,kwargs=kwargs).start()
    return x

def on_cmd(data):
    async def func(flt, _, message):
        if str(message.chat.id) not in blacklisted_chats and message.text is not None and message.from_user is not None:
            return message.from_user.is_self and message.text.split()[0] == f'{COMMAND_PREFIX}{flt.data}'
    return filters.create(func, data=data)

app = Client(
    name=None,
    session_string=config["SESSION_STRING"],
    api_id=config["API_ID"],
    api_hash=config["API_HASH"])
