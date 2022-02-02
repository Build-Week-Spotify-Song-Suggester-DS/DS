import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import getenv
from .models import DB, Track

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
    '''Returns dictionary with information about the track'''
    result = sp.audio_features(track_id)[0]
    result['name'] = sp.track(track_id)['name']
    result['artists'] = sp.track(track_id)['artists'][0]['name']
    return result


def add_track_to_db(track_id, preference=False):
    try:

        already_exists = Track.query.filter(Track.id == track_id).all()
        if already_exists:
            print(f'{track_id} already in database, skipping...')
        else:
            other_info = find_track_info(track_id)

            new_preference = Track(id=track_id,
                                   preference=preference,
                                   name=other_info['name'],
                                   artists=other_info['artists'],
                                   danceability=other_info['danceability'],
                                   energy=other_info['energy'],
                                   key=other_info['key'],
                                   loudness=other_info['loudness'],
                                   mode=other_info['mode'],
                                   speechiness=other_info['speechiness'],
                                   acousticness=other_info['acousticness'],
                                   instrumentalness=other_info['instrumentalness'],
                                   liveness=other_info['liveness'],
                                   valence=other_info['valence'],
                                   tempo=other_info['tempo'],
                                   duration_ms=other_info['duration_ms'],
                                   time_signature=other_info['time_signature'])
            DB.session.add(new_preference)

    except Exception as error:
        print(f"Could not add {other_info['name']} to database: {error}")
        raise error
    else:
        DB.session.commit()


def update_tracks_in_db(num_tracks=1000):
    '''Adds new hipster tracks 
       directly to the database
       with all information updated
       (very slow)'''

    # Request Cap
    num_tracks = min(num_tracks, 1000)

    # Parameters
    max_tracks_per_album = 3

    # Remove old tracks
    try:
        Track.query.filter(Track.preference == False).delete()
    except Exception as error:
        print(f'error deleting tracks: {error}')
        raise error
    else:
        DB.session.commit()

    i = 0  # num_tracks added
    j = 0  # number of albums looked at
    while i < num_tracks:
        # Find Hipster Albums
        albums = sp.search(q="tag:hipster",
                           type='album',
                           limit=10,
                           offset=j)['albums']['items']
        # Find Tracks in each Album
        for album in albums:
            tracks = sp.album_tracks(album['id'],
                                     limit=max_tracks_per_album)['items']
            # Add each Track to Database
            for result in tracks:
                add_track_to_db(track_id=result['id'])
                i += 1
                # stops searching tracks after num_tracks
                if i >= num_tracks:
                    break
            # stops searching albums after num_tracks
            if i >= num_tracks:
                break
        # Update offset index for next set of albums
        j += 10
    return
