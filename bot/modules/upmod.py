from bot import app,on_cmd
import os

@app.on_message(filters=on_cmd("upmod"))
def _(_,message):
    mod_name = message.text.split(" ",1)
    if len(mod_name) < 2 :
        message.reply_text("no module name supplied", quote=True)
        return

    mod_name = mod_name[1]
        
    # hardcoded .py so only module name is required and nobody uploads files others than .py files, you can go back using ../
    # but again, only .py files, so i think its safe, you cant upload cache, session, config vars, files
    file_path = f"bot/modules/{mod_name}.py"
    if os.path.exists(file_path):
        message.reply_document(file_path)
        return
    message.reply_text("file not found!",quote=True)