from threading import Thread
from pyrogram import Client, idle
from pyrogram import filters
import os
import logging
from dotenv import dotenv_values

config = {
    **dotenv_values(),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

logging.basicConfig(level=logging.INFO)

# pyrogram client
session_string = config["SESSION_STRING"]
app = Client(
    name=None,
    session_string=session_string,
    api_id=config["API_ID"],
    api_hash=config["API_HASH"])


blacklisted_chats = [ k.strip() for k in config.get("BLACKLISTED_CHATS","").split(",") ]

def main():
    #start the client first
    app.start()

    # this function map is the workaround/fix for eval is evil, but still uses eval to be made, pretty ironic :P
    # map/dict of all functions/modules available in ./modules folder
    function_map = {}
    for i in modules.loadable_mods:
        function_map[f".{str(i)}"] = eval(f"{i}.{i}")
    backup_function_map = function_map.copy()

    # message filter to check if the message is from user and has `text` at the start
    def dynamic_data_filter(data):
        async def func(flt, _, message):
            if str(message.chat.id) not in blacklisted_chats and message.text is not None and message.from_user is not None:
                return message.from_user.is_self and message.text.startswith(flt.data)
        return filters.create(func, data=data)

    @app.on_message(dynamic_data_filter(".disable"))
    async def _(_,message):
        args = message.text.split()
        for i in args[1:]:
            i = f".{i}"
            if i in function_map:
                function_map.pop(i)
                await message.reply_text(f"`disabled module {i}`")
            else:
                await message.reply_text(f"`module {i} not loaded...`")

    @app.on_message(dynamic_data_filter(".enable"))
    async def _(_,message):
        args = message.text.split()
        for i in args[1:]:
            i = f".{i}"
            if i in backup_function_map:
                function_map.update({i : backup_function_map[i]})
                await message.reply_text(f"`loaded module {i}!`")
            else:
                await message.reply_text(f"`module {i} not found to load...`")

    # unloads/loads all the modules, runnable scripts will still be running
    @app.on_message(dynamic_data_filter(".stop"))
    async def _(_,message): function_map.clear() ; await message.reply_text(f"`paused all modules!`")
    
    @app.on_message(dynamic_data_filter(".start"))
    async def _(_,message): function_map.update(backup_function_map) ; await message.reply_text(f"`loaded all modules!`")

    # help function
    @app.on_message(dynamic_data_filter(".help"))
    async def _(_, message):
        method = message.text.split(None,1)[1]
        if f".{method}" in backup_function_map.keys(): await message.reply_text(eval(f"{method}.help"),quote=True)
        else : await message.reply_text(f"module {method} not found")

    # on message listener and function execute ONLY if its in function_map
    @app.on_message(dynamic_data_filter("."))
    async def _(client, message):
        method = message.text.split(None,1)[0]
        if method in function_map.keys():
            Thread(target=function_map[method],args=(client,message)).start()

    # start all the runnable threads
    for i in modules.runnable_scripts:
        t = Thread(target=eval(f"{i}.runnable"),args=(app,))
        t.daemon = True
        t.start()

    # keep running
    idle()

if __name__ == "__main__":
    from modules import *
    import modules
    main()