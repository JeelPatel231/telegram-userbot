from datetime import datetime

def ping(_,mess):
    start = datetime.now()
    mess.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    mess.edit(f"`Pong!\n{duration}ms`")