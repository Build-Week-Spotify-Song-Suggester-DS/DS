import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import getenv

CLIENT_ID = getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                                      client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def search_tracks(artist=None, name=None):
    '''Returns a list of dictionaries
       Each dictionary contains a track's
       id, name, artists, and album
    '''
    tracks = []

    # generate query string
    query = ''
    if artist:
        query += f'artist:{artist}'
        if name:
            query += f' track:{name}'
    else:
        if name:
            query += f'track:{name}'
        else:
            print('error: no search parameters entered')
            return

    # results are limited to 1000 items
    #  and each search will only return 50 items
    #  so we have to loop over them with an offset index

    for i in range(0, 1000, 50):
        result = sp.search(q=query,
                           type='track',
                           limit=50,
                           offset=i)['tracks']['items']
        for track in result:
            tracks.append({'id': track['id'],
                           'name': track['name'],
                           'artists': track['artists'][0]['name'],
                           'album': track['album']['name']})

        # stops querying if spotify is out of results
        if len(result) < 50:
            break
    return tracks


def find_track_info(track_id):
    # Returns dictionary with information about the track
    result = sp.audio_features(track_id)[0]
    result['name'] = sp.track(track_id)['name']
    result['artists'] = sp.track(track_id)['artists'][0]['name']
    return result


def new_tracks():
    # WIP
    '''Returns a list of 1000 tracks
       stored in dictionaries containing
       id, name, artists, album, and
       audio_features (danceability etc.)
    '''
    tracks = []
    for i in range(0, 1000, 50):
        result = sp.search(q="tag:new",
                           type='track',
                           limit=50,
                           offset=i)  # ['tracks']['items']
        # print(result)
        for track in result:
            tracks.append(find_track_info(track['id']))
    return tracks
