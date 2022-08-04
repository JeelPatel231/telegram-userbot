from __future__ import unicode_literals
from bot import app, on_cmd
import yt_dlp
import os

def download(url,audio:bool = False):
    ydl_opts = {
        'outtmpl': 'temp/%(title)s.%(ext)s',
    }

    if audio: ydl_opts.update({
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@app.on_message(filters=on_cmd("ytdl"))
def ytdl(_,message):
    if message.reply_to_message is not None:
        link = message.reply_to_message.text
    else:
        link = message.text.split(" ")[-1]
        if "http" not in link:
            message.reply_text("Unable to find link, perhaps add or reply to one?",quote=True)
            return
    audio = ("-a" in message.text)

    message.reply_text(f"Starting Download.",quote=True)
    try:
        filename = download(link,audio)
    except Exception as e:
        message.reply_text("Error Occured: \n"+str(e),quote=True)
        return

    message.reply_text(f"Downloaded {filename}.\nStarting Upload.",quote=True)

    if audio:
        message.reply_audio(filename.rsplit('.')[0]+".mp3",quote=True)
    else:
        message.reply_video(filename,quote=True)
    
    for file in os.listdir("temp"):
        os.remove(f"temp/{file}")
