from bot import app, on_cmd
from io import StringIO
import sys

@app.on_message(filters=on_cmd("run"))
def _(_,message):
    cmd = message.text.split(None,1)[1]
    try:
        sys.stdout = StringIO()
        exec(cmd)
        resp = sys.stdout.getvalue()
    except Exception as e:
        print(e)
        resp = str(repr(e))

    if resp != "":
        message.reply_text(resp,quote=True)