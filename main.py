from pyrogram import Client
from pyrogram import filters
from modules import *
import modules
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

# pyrogram client
session_string = os.environ["SESSION_STRING"]
app = Client(
    session_string,
    api_id=os.environ["API_ID"],
    api_hash=os.environ["API_HASH"]
)

# this function map is the workaround/fix for eval is evil, but still uses eval to be made, pretty ironic :P
# map/dict of all functions/modules available in ./modules folder
function_map = {}
for i in modules.__all__:
    function_map[f".{str(i)}"] = eval(f"{i}.{i}")

# message filter to check if the message is from user and has "." at the start
async def message_filter(_,__,message):
    if message.text is not None and message.from_user is not None:
        return message.from_user.is_self and message.text.startswith('.')


# on message listener and function execute ONLY if its in function_map
@app.on_message(filters.create(message_filter))
async def my_function(client, message):
    method = message.text.split(" ",1)[0]
    if method in function_map.keys():
        await function_map[method](client,message)

# :P
app.run()