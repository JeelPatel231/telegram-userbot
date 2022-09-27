import os
from bot import app, on_cmd, config
import requests
from PIL import Image


@app.on_message(filters=on_cmd("rbg"))
def _(client,mess):
    # TODO : IN MEMORY DOWNLOAD AND UPLOAD

    if config.get("REMBG_API_KEY") is None:
        mess.reply_text("get the api key first and set as REMBG_API_KEY in environment!",quote=True)
        return 

    file_path = client.download_media(mess.reply_to_message)

    if not file_path.endswith((".jpg",".png")):
        k = Image.open(file_path)
        k = k.convert("RGB")
        os.remove(file_path)
        file_path = file_path.rsplit('.')[0]+".png"
        k.save(file_path)

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(file_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': config.get("REMBG_API_KEY")},
    )

    os.remove(file_path)
    if response.status_code == requests.codes.ok:
        with open('pastes/no-bg.png', 'wb') as out:
            out.write(response.content)
        mess.reply_document("pastes/no-bg.png",quote=True)
        os.remove("pastes/no-bg.png")
    else:
        mess.reply_text(f"Error: {response.status_code} {response.text}", quote=True)