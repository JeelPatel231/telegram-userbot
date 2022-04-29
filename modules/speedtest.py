from speedtest import Speedtest

def speedtest(_,mess):
    mess.edit("`Running Speedtest...`")
    st = Speedtest()
    dl = st.download()/1048576
    ul = st.upload()/1048576 if "-u" in mess.text else None
    res = f"`Results:\nDL = {dl:.2f} mbps\n`"
    if ul is not None: res += f"`UP = {ul:.2f} mbps`" 
    mess.edit(res)

help = "`starts a speedtest`"