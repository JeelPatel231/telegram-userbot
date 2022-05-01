import re

def calc(_,mess):
    text = mess.text.split(' ',1)[1]
    if re.search('[a-zA-Z]', text ) is None:
        mess.reply_text(eval(text), quote=True)
        return
    mess.reply_text("`alphabets detected, calc rejected!`", quote=True)