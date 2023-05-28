from dotenv import load_dotenv
import os
from collections import Counter
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import datetime

# Load environment variables
load_dotenv()

# set authentication
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# df for data
artists_df = pd.DataFrame(columns=['Id', 'Name', 'Popularity', 'Genres', 'Followers'])
top_songs_df = pd.DataFrame(columns=['Id', 'Name', 'Album_id', 'Artist_Id' , 'Popularity', 'Duration', 'IsSingle'])

# get the spotify api 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

charts_dict = {
    'Global': '37i9dQZEVXbMDoHDwVN2tF',
    'USA': '37i9dQZEVXbLRQDuF5jeBp',
    'UK': '37i9dQZEVXbLnolsZ8PSNw',
    'Italy': '37i9dQZEVXbIQnj7RRhdSX',
    'Germany': '37i9dQZEVXbJiZcmkrIHGU',
    'France': '37i9dQZEVXbIPWwFssbupI',
    'Spain': '37i9dQZEVXbNFJfN1Vw8d9',
    'Netherlands': '37i9dQZEVXbKCF6dqVpDkS',
    'Iceland': '37i9dQZEVXbKMzVsSGQ49S',
    'Switzerland': '37i9dQZEVXbJiyhoAPEfMK'
}

# tuple for matching the charts playlists with their corresponding id

# get the top artists 
def get_top_artists():
    # get Top 50 Artists in Json format
    results = sp.search(q='year:2022', type='artist', limit=50)

    dic_list = []

    # Loop through the Json document and store in df
    for artist in results['artists']['items']:
        id = artist['id']
        name = artist['name']
        popularity = artist['popularity']
        genres = artist['genres']
        followers = artist['followers']['total']
        
        tmp_dict = {'Id': id,
                    'Name': name,
                    'Popularity': popularity,
                    'Genres': genres,
                    'Followers': followers}
        dic_list.append(tmp_dict)

    return pd.DataFrame.from_records(dic_list)

def get_top_songs(df_artists):

    dic_list = []

    for index, row in df_artists.iterrows():
        results = sp.artist_top_tracks(row['Id'])

        for song in results['tracks']:
            id = song['id']
            name = song['name']
            album_id = song['album']['id']
            artist_id = song['artists'][0]['id']
            popularity = song['popularity']
            duration = song['duration_ms']
            isSingle = song['album']['album_type']

            tmp_dict = {'Id': id,
                        'Name': name,
                        'Album_id': album_id,
                        'Artist_id': artist_id,
                        'Popularity': popularity,
                        'Duration': duration,
                        'isSingle': isSingle}
            
            dic_list.append(tmp_dict)
        
    return pd.DataFrame.from_records(dic_list)

def get_artist_albums(df_artists):
    
    dic_list = []

    for index, row in df_artists.iterrows():
        results = sp.artist_albums(row['Id'])

        for album in results['items']:
            id = album['id']
            name = album['name']
            release_date = album['release_date']
            total_tracks = album['total_tracks']
            artist_id = album['artists'][0]['id']

            tmp_dict = {'Id':id,
                        'Name':name,
                        'Release_date': release_date,
                        'Total_tracks': total_tracks,
                        'Artist_id': artist_id}
            dic_list.append(tmp_dict)
    
    return pd.DataFrame.from_records(dic_list)
            
def get_top_songs_for_country(country):
    
    counter = 1
    playlist_id = charts_dict.get(country)
    results = sp.playlist(playlist_id)
    dic_list= []

    for track in results['tracks']['items']:
        id = track['track']['id']
        name = track['track']['name']
        release_date = track['track']['album']['release_date']
        artist = track['track']['artists'][0]['name']
        artist_id = track['track']['artists'][0]['id']
        popularity = track['track']['popularity']
        duration = track['track']['duration_ms']
        album_id = track['track']['album']['id']
        isSingle = track['track']['album']['album_type']

        artist_info = sp.artist(artist_id)
        genres = ', '.join(str(i) for i in artist_info['genres'])

        audio_features = sp.audio_features(id)

        danceability = audio_features[0]['danceability']
        energy = audio_features[0]['energy']
        speechiness = audio_features[0]['speechiness']
        acousticness = audio_features[0]['acousticness']
        instrumentalness = audio_features[0]['instrumentalness']
        liveness = audio_features[0]['liveness']
        valence = audio_features[0]['valence']
        tempo = audio_features[0]['tempo']
        last_refresh = datetime.date.today()


        tmp_dict = {    'Country' : country,
                        'Rank' : counter,
                        'Id': id,
                        'Name': name,
                        'Release_date' : release_date,
                        'Album_id': album_id,
                        'Artist': artist,
                        'Artist_id': artist_id,
                        'Genres': genres,
                        'Popularity': popularity,
                        'Duration': duration,
                        'IsSingle': isSingle,
                        'Danceability' : danceability,
                        'Energy' : energy,
                        'Speechiness' : speechiness,
                        'Acousticness' : acousticness,
                        'Instrumentalness' : instrumentalness,
                        'Liveness' : liveness,
                        'Valence' : valence,
                        'Tempo' : tempo,
                        'Last_refresh': last_refresh
                        }
            
        dic_list.append(tmp_dict)
        counter = counter + 1

    return pd.DataFrame.from_records(dic_list)



