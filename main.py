import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

billboard_url = "https://www.billboard.com/charts/hot-100/"
Client_ID = "Client ID"
Client_Secret = "Client Secret"
redirect_URI = "http://example.com"

date = input("Which year do you want?Type the date in this format YYYY-MM-DD: ")

URL = ("https://www.billboard.com/charts/hot-100/" + date)
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
all_music = soup.select("li ul li h3")
record = [music.getText().replace("\n", "").strip() for music in all_music]

# print(record)

# -------------------Spotify Authentication and token.txt creation ----------------------#
spotify_auth = spotipy.oauth2.SpotifyOAuth(client_id=Client_ID,
                                           client_secret=Client_Secret,
                                           redirect_uri=redirect_URI,
                                           scope="playlist-modify-private",
                                           show_dialog=True,
                                           cache_path="token.txt"
                                           )
spotify_auth.get_access_token(as_dict=False)
s = spotipy.Spotify(oauth_manager=spotify_auth)
user_id = s.current_user()["id"]

# --------------------Searching Spotify for the songs----------------------------#
song_uris = []
year = date.split("-")[0]
for song in record:
    result = s.search(q=f"track:{song} year:{year}", type="track", limit=1)
    # print(result)
    try:
        # Handling exception where the song cannot be found. It is skipped in this case.
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
