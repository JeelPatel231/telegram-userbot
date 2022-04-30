import os

def upmod(_,message):
    mod_name = message.text.split(" ",1)[1]
    # hardcoded .py so only module name is required and nobody uploads files others than .py files, you can go back using ../
    # but again, only .py files, so i think its safe, you cant upload cache, session, config vars, files
    file_path = f"modules/{mod_name}.py"
    if os.path.exists(file_path):
        message.reply_document(file_path)
        return
    message.reply_text("file not found!",quote=True)