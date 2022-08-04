import subprocess
from bot import app,on_cmd

FALLBACK_URL = "https://github.com/jeelpatel231/telegram-userbot"

@app.on_message(filters=on_cmd("repo"))
def _(_,mess):
    op = subprocess.run(['git','remote','get-url','origin'], capture_output=True)

    if op.stderr != b'' or op.stdout == b'':
        print(".repo : SWITCHING TO FALLBACK")
        op = FALLBACK_URL
    else:
        op = op.stdout.decode("utf-8")

    mess.reply_text(op, quote=True, disable_web_page_preview=True)