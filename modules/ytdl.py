from __future__ import unicode_literals
import youtube_dl
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

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

def ytdl(client,message):
    try:
        link = message.text.split(" ")[-1]
    except IndexError:
        if message.reply_to_message is not None:
            link = message.reply_to_message.text
        else:
            message.reply_text("Unable to find link, perhaps add or reply to one?")
            return
    audio = ("-a" in message.text)

    message.reply_text(f"Starting Download.")
    filename = download(link,audio)
    message.reply_text(f"Downloaded {filename}.\nStarting Upload.")

    if audio:
        client.send_audio(message.chat.id,filename.rsplit('.')[0]+".mp3")
    else:
        client.send_video(message.chat.id,filename)
    
    for file in os.listdir("temp"):
        os.remove(f"temp/{file}")