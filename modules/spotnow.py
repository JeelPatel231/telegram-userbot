from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
from urllib.request import urlopen
import spotipy
import spotipy.util as util

# set SPOTIPY_CLIENT_SECRET & SPOTIPY_CLIENT_ID
token = util.prompt_for_user_token(scope='user-read-currently-playing', redirect_uri="http://localhost:8000/callback")
spotify = spotipy.Spotify(auth=token)

font_24 = ImageFont.truetype("modules/assets/GoNotoCurrent.ttf", size=25)
font_20 = ImageFont.truetype("modules/assets/GoNotoCurrent.ttf", size=20)

def get_details() -> tuple:
    current_track = spotify.current_user_playing_track()
    if current_track == None:
        return None
    complete_percent = current_track["progress_ms"]/current_track["item"]["duration_ms"]
    current_track = current_track["item"]
    song_name = current_track["name"]
    artists = ", ".join([artist["name"] for artist in current_track["artists"]])
    album_name = current_track["album"]["name"]
    track_id = current_track["id"] # unique song identifier
    image = current_track["album"]["images"][1]["url"]
    link = current_track["external_urls"]["spotify"]
    return (song_name,artists,album_name,image,link,complete_percent,track_id)

def make_image(data,username) -> BytesIO:
    canvas = Image.new('RGB', (600,250))
    draw = ImageDraw.Draw(canvas)

    album_art = Image.open(urlopen(data[3])) # 300px image
    blurred_art = album_art.filter(ImageFilter.GaussianBlur(5))
    blurred_art = blurred_art.resize((600,600))
    blurred_art = ImageEnhance.Brightness(blurred_art).enhance(0.6)
    canvas.paste(blurred_art,(0,-175))
    album_art = album_art.resize((200, 200)) # resize to 200px
    canvas.paste(album_art, (25,25)) # paste at 25,25

    # Write text
    draw.text((240, 25), username, font=font_24, fill=(255,255,255))
    draw.text((240, 60), "is listening to", font=font_20, fill=(255,255,255))
    draw.text((240, 115), data[0], font=font_24, fill=(255,255,255))
    draw.text((240, 150), data[1], font=font_20, fill=(255,255,255))
    draw.text((240, 180), data[2], font=font_20, fill=(255,255,255))

    # draw completion line
    draw.line([(240,220),(540,220)],fill="grey",width=4)
    draw.line([(240,220),(240+(300*data[5]),220)],fill="white",width=4)

    file_bytes = BytesIO()
    canvas.save(file_bytes,format="png")

    return file_bytes

def spotnow(_,message):
    data = get_details()
    if data == None:
        message.reply_text("listening nothing at the moment...",quote=True)
        return
    file = make_image(data,message.from_user.first_name)
    message.reply_photo(file,caption=f"[Track link]({data[4]})",quote=True)
