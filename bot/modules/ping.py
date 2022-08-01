from bot import app, on_cmd
from datetime import datetime

@app.on_message(filters=on_cmd("ping"))
def _(client,mess):
    start = datetime.now()
    ping_mess = client.send_message("me","ping test")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    mess.reply_text(f"`Pong!\n{duration}ms`",quote=True)
    ping_mess.delete()

@app.on_message(filters=on_cmd("help ping"))
def _(_,m):
    m.reply_text("`pingtest to nearest TG DC`", quote=True)
