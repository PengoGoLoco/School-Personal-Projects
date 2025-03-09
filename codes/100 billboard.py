from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# User Input
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Scrape Billboard Hot 100
header = {"User-Agent": "Mozilla/5.0"}
billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url=billboard_url, headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id="YOUR-CLIENT-ID",
        client_secret="YOUR-CLIENT-SECRET",
        show_dialog=True,
        cache_path="token.txt"
    )
)

# Get User ID
user_id = sp.current_user()["id"]

# Search Songs on Spotify
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create Playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# Add Songs to Playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

print(f"Playlist '{date} Billboard 100' created successfully!")
