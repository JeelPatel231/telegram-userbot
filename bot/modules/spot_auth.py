import spotipy
from bot import app,on_cmd, config
from spotipy.oauth2 import SpotifyOAuth
from spotipy import CacheFileHandler
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from urllib.request import urlopen
from io import BytesIO

client_id = config.get("SPOTIPY_CLIENT_ID")
client_secret = config.get("SPOTIPY_CLIENT_SECRET")
redirect_uri = config.get("SPOTIPY_REDIRECT_URI")
scope = "user-read-currently-playing"

font_24 = ImageFont.truetype("bot/assets/GoNotoCurrent.ttf", size=25)
font_20 = ImageFont.truetype("bot/assets/GoNotoCurrent.ttf", size=20)

authlink = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
cfh = CacheFileHandler()
sp_oauth = spotipy.SpotifyOAuth(client_id,client_secret,redirect_uri,scope=scope,cache_handler=cfh)

spotify = None

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

@app.on_message(filters=on_cmd("spotnow"))
def spotnow(_,m):
    global spotify
    if spotify is None: # not initialized yet
        token_info = cfh.get_cached_token() # get cached token

        if token_info is None: # if no cached token availabled
            m.reply_text(f"renew token, click the link and you will get redirected to a url.\nuse it as '.spotauth <url>'\n {authlink}")
            return

        if sp_oauth.is_token_expired(token_info): # token available but expired
            sp_oauth.refresh_access_token(token_info["refresh_token"]) # renew it :P
            return

        spotify = spotipy.Spotify(auth=token_info["access_token"]) # use token and get details
    
    data = get_details()
    if data == None:
        m.reply_text("listening nothing at the moment...",quote=True)
        return

    file = make_image(data,m.from_user.first_name)
    m.reply_photo(file,caption=f"[Track link]({data[4]})",quote=True)


@app.on_message(filters=on_cmd("spotauth"))
def auth_proc(_,m):

    spli =  m.text.split(" ")
    if len(spli) != 2:
        m.reply_text("give redirect url you dumbfuck!")
        return

    code = SpotifyOAuth.parse_auth_response_url(spli[1])
    token = sp_oauth.get_access_token(code, as_dict=False)

    global spotify
    spotify = spotipy.Spotify(auth=token)
    
    cur_user = spotify.current_user()
    txt = f'Authorised as [{cur_user["display_name"]}]({cur_user["external_urls"]["spotify"]})'
    m.reply_text(txt, quote=True)
