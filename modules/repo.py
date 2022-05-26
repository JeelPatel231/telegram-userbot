import subprocess

FALLBACK_URL = "https://github.com/jeelpatel231/telegram-userbot"

def repo(_,mess):
    op = subprocess.run(['git','remote','get-url','origin'], capture_output=True)

    if op.stderr != b'' or op.stdout == b'':
        op = FALLBACK_URL
    else:
        op = op.stdout.decode("utf-8")

    mess.reply_text(op, quote=True, disable_web_page_preview=True)