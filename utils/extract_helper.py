import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config
import pandas as pd
from IPython.display import display
import datetime
import hashlib
from uuid import uuid4
import logging

from connect_database import get_session
from models import Track

logging.basicConfig(level=logging.DEBUG)

# enviroment variables
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = config('SPOTIFY_REDIRECT_URI')


def generate_hash(string):
    return hashlib.md5(string.encode()).hexdigest()


def spotify_extract_info():

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope='user-read-recently-played'
    ))
    data = sp.current_user_recently_played(limit=50)

    if len(data) == 0:
        print('data not found')
    else:
        album_list = []
        for row in data["items"]:
            album_id = row['track']['album']['id']
            album_name = row['track']['album']['name']
            album_url = row['track']['album']['external_urls']['spotify']
            album_release_date = row['track']['album']['release_date']
            album_total_tracks = row['track']['album']['total_tracks']

            element = {
                'album_id': album_id,
                'album_name': album_name,
                'album_url': album_url,
                'album_release_date': album_release_date,
                'album_total_tracks': album_total_tracks,
            }

        album_list.append(element)

        id_list = []
        name_list = []
        url_list = []

        for item in data['items']:
            for key, value in item.items():
                if key == 'track':
                    for point in value['artists']:
                        id_list.append(point['id'])
                        name_list.append(point['name'])
                        url_list.append(point['external_urls']['spotify'])
        artist_dict = {
            'artist_id': id_list,
            'artist_name': name_list,
            'url_list': url_list,
        }

        # print(artist_dict)

        # canciones
        # crear la estructura de datos para los tracks
        # id, name, url, popularity, duration_ms, album_id, artist_id, played_at
        track_list = []
        for row in data["items"]:
            track_id = row['track']['id']
            track_name = row['track']['name']
            track_url = row['track']['external_urls']['spotify']
            track_popularity = row['track']['popularity']
            track_duration_ms = row['track']['duration_ms']
            track_played_at = row['played_at']
            track_album_id = row['track']['album']['id']
            track_artists_id = []
            for artist in row['track']['artists']:
                track_artists_id.append(artist['id'])

            hash = str(track_id) + str(track_name) + str(track_url) + str(track_popularity) + \
                str(track_duration_ms) + \
                str(track_album_id)

            track_element = {
                'track_id': track_id,
                'track_name': track_name,
                'track_url': track_url,
                'track_popularity': track_popularity,
                'track_duration_ms': track_duration_ms,
                'track_played_at': track_played_at,
                'track_album_id': track_album_id,
                'track_artists_id': track_artists_id,
                'id_unique': generate_hash(hash),
            }

            track_list.append(track_element)

        # Cargar los datos desde la entidad album a un dataframe
        album_df = pd.DataFrame.from_dict(data=album_list)

        # Cargar los datos desde la entidad track a un dataframe
        track_df = pd.DataFrame.from_records(data=track_list)
        display(track_df)

        # Borrar duplicados album
        album_df = album_df.drop_duplicates(subset=['album_id'])

        # Borrar duplicados del artista
        artist_df = pd.DataFrame.from_records(data=artist_dict)
        artist_df = artist_df.drop_duplicates(subset=['artist_id'])

        # Fechas
        # Cambiar la fecha por timestamp
        #track_df['track_played_at'] = pd.to_datetime(track_df['track_played_at'])
        track_df['track_played_at'] = pd.to_datetime(
            track_df['track_played_at'])
        track_df['track_played_at'] = track_df['track_played_at'].dt.strftime(
            '%m/%d/%Y')

        # crear load data
        track_df['load_data'] = datetime.datetime.now()
        track_df['load_data'] = track_df['load_data'].dt.strftime('%m/%d/%Y')
        track_df = track_df.drop_duplicates(subset=['id_unique'])

        # cargar data en cvs
        track_df.to_csv('tracks.csv', index=False, header=True)

        # cargar data en excel
        track_df.to_excel('tracks.xlsx', index=False, header=True)

        session = get_session()

        with session:
            session.begin()
            try:
              for index, row in track_df.iterrows():
                 new_track=Track(name=row["track_name"])
                 session.add(new_track)
            except:
              session.rollback()
              raise
            else:
              session.commit()

       


spotify_extract_info()
