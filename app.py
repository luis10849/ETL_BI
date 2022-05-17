from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config
import spotipy

client_id = config('CLIENT_ID')
client_secret = config('CLIENT_SECRET')

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
result = sp.search('Radiohead')
song = result['tracks']['items']
print(result)