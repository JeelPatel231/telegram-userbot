from pyrogram import idle
from bot import app
from .modules import *
from .modules import runnable_scripts
from threading import Thread

def main():
    #start the client first
    app.start()

    # start all the runnable threads
    for i in runnable_scripts:
        t = Thread(target=eval(f"{i}.runnable"),args=(app,))
        t.daemon = True
        t.start()

    # keep running
    idle()

if __name__ == "__main__":
    main()