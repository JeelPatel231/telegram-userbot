import time
import psycopg
from decimal import Decimal
import os
from .spotnow import get_details
from .spotnow import make_image

OFFSET = 1650705548 # 3 day span in epoch
INSERT_QUERY = "INSERT INTO spotifypublishdata (track_id,last_played) VALUES (%s,CURRENT_TIMESTAMP)"
UPDATE_QUERY = "UPDATE spotifypublishdata SET last_played = CURRENT_TIMESTAMP where track_id = %s"
SELECT_QUERY = "select extract(epoch from last_played) from spotifypublishdata WHERE track_id=%s"
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS spotifyPublishData ( track_id VARCHAR(50) PRIMARY KEY, last_played TIMESTAMP )"
POLL_INTERVAL = 30

def runnable(client):
    try:
        conn = psycopg.connect(os.environ["POSTGRES_URL"])
    except:
        print("Exception Occurred in spotify Publisher, script will not be executed further")
        client.send_message("me","Exception Occurred in spotify Publisher, script will not be executed further")
        return
    chat_id = os.getenv("SPOTIFY_PUBLISH_CHAT_ID","me")
    cur = conn.cursor()

    cur.execute(CREATE_TABLE)
    conn.commit()

    while True:
        print("POLLED")
        data = get_details()
        if data == None:
            time.sleep(POLL_INTERVAL)
            continue
        result = cur.execute(SELECT_QUERY,(data[6],)).fetchall()
        if result == []:
            cur.execute(INSERT_QUERY,(data[6],))
            conn.commit()
            photo = make_image(data,client.get_me().username)
            client.send_photo(chat_id,photo,caption=f"[HERE]({data[4]})")
        elif Decimal(time.time()) - result[0][0] > OFFSET:
            cur.execute(UPDATE_QUERY,(data[6],))
            conn.commit()
            photo = make_image(data,client.get_me().username)
            client.send_photo(chat_id,photo,caption=f"[HERE]({data[4]})")
        time.sleep(POLL_INTERVAL)