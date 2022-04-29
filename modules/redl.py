import os, requests, json

def redl(_,message):
    try:
        link = message.reply_to_message.text.split("?")[0] # remove query parameters
        if "redd.it" in link:
            link = f"https://www.reddit.com/comments/{link.split('/')[-1]}/" # directly get the redirect url for json
    except:
        message.reply_text("reply to a link pl0x..")
        return
    
    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'}

    try:
        json_response = requests.get(f"{link}.json",headers=headers).json()
    except:
        message.reply_text("error in Request to fetch json!",quote=True)
        return

    media = json_response[0]["data"]["children"][0]["data"]
    title = media["title"]
    if not media["is_video"]:
        message.reply_photo(media["url_overridden_by_dest"],quote=True,caption=title)
    else:
        link = media["media"]["reddit_video"]["dash_url"]
        output = os.popen(f"ffprobe -show_streams -show_entries stream=index,codec_type -of json -v quiet -i '{link}'").read()
        arr = json.loads(output)["streams"]
        audio_index,video_index = arr[-1]["index"], arr[-2]["index"]
        abspath = os.path.abspath("temp/output.mp4")
        exit_code = os.system(f"ffmpeg -i '{link}' -map 0:{video_index} -map 0:{audio_index} -codec copy '{abspath}'")
        
        if not exit_code:
            message.reply_video(abspath,quote=True,caption=title)
            os.remove(abspath)
            return
        message.reply_text("Some error occured, check logs")

help = "`Download Reddit media (photos/videos)`"