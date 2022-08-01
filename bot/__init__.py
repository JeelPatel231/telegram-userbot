from threading import Thread
from pyrogram import Client
from dotenv import dotenv_values
import os
import logging

config = {
    **dotenv_values(),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

logging.basicConfig(level=logging.INFO)

def run_threaded(fn):
    def x(*args, **kwargs):
        Thread(target=fn,args=args,kwargs=kwargs).start()
    return x

app = Client(
    name=None,
    session_string=config["SESSION_STRING"],
    api_id=config["API_ID"],
    api_hash=config["API_HASH"])
