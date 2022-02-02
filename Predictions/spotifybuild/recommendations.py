import spotipy
import requests
from os import getenv
from spotipy.oauth2 import SpotifyClientCredentials

client_id = getenv('SPOTIPY_CLIENT_ID')
client_secret = getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def feature_vectors(track_id):
    track_features = spotipy.audio_features(track_id)

    feature_vector = list(track_features.values())
    feature_names = list(track_features.keys())

    return feature_names, feature_vector