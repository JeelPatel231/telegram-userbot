import spotipy
import spotipy.util as util

username = "Jeel Patel"
# set SPOTIPY_CLIENT_SECRET & SPOTIPY_CLIENT_ID
token = util.prompt_for_user_token(username, 'user-read-currently-playing', redirect_uri="http://localhost:8000/callback")
spotify = spotipy.Spotify(auth=token)

def getDetails() -> tuple:
    current_track = spotify.current_user_playing_track()["item"]
    song_name = current_track["name"]
    artists = ", ".join([artist["name"] for artist in current_track["artists"]])
    album_name = current_track["album"]["name"]
    track_id = current_track["id"] # unique song identifier
    image = current_track["album"]["images"][0]["url"]

    return (song_name,artists,album_name,track_id,image)

def spotnow(_,message):
    data = getDetails()
    message.reply_photo(data[4],caption=f"SONG     :   {data[0]}\nARTISTS :   {data[1]}\nALBUM  :   {data[2]}",quote=True)
