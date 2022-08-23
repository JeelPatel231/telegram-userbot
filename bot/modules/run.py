from bot import app, on_cmd
from io import StringIO
import sys

@app.on_message(filters=on_cmd("run"))
def _(client,message):
    cmd = message.text.split(None,1)[1]
    try:
        sys.stdout = StringIO()
        exec(cmd)
        resp = sys.stdout.getvalue()
    except Exception as e:
        print(e)
        resp = str(repr(e))

    if resp.__len__() == 0: return

    if resp.__len__() > 1024:
        with open("pastes/output.txt","w") as file:
            file.write(resp)
        message.reply_document("pastes/output.txt",quote=True)
        return

    message.reply_text(resp,quote=True)