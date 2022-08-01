from bot import app, on_cmd
import re

@app.on_message(filters=on_cmd("calc"))
def _(_,mess):
    text = mess.text.split(' ',1)[1]
    if re.search('[a-zA-Z]', text ) is None:
        mess.reply_text(eval(text), quote=True)
        return
    mess.reply_text("`alphabets detected, calc rejected!`", quote=True)

@app.on_message(filters=on_cmd("help calc"))
def _(_,m):
    m.reply_text("`its a calculator, thats it`", quote=True)
