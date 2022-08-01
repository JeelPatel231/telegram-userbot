from bot import app, on_cmd
from speedtest import Speedtest

@app.on_message(filters=on_cmd("speedtest"))
def _(_,mess):
    mess.edit("`Running Speedtest...`")
    st = Speedtest()
    dl = st.download()/1048576
    ul = st.upload()/1048576 if "-u" in mess.text else None
    res = f"`Results:\nDL = {dl:.2f} mbps\n`"
    if ul is not None: res += f"`UP = {ul:.2f} mbps`" 
    mess.reply_text(res,quote=True)

@app.on_message(filters=on_cmd("help speedtest"))
def _(_,m):
    m.reply_text("`starts a speedtest`", quote=True)