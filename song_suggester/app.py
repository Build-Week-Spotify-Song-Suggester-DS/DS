from flask import Flask, render_template, request
from os import getenv
from .models import DB, Track
from .spotify import search_tracks, find_track_info, new_tracks


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect the DB to the app
    DB.init_app(app)

    @app.route("/", methods=['GET', 'POST'])
    def home_page(track_search=None,
                  artist_search=None,
                  search_results=None,
                  preferences=None,
                  recommendations=None):

        # Database Initialization
        DB.create_all()

        # Form Requests
        if request.method == 'POST':

            # Search Form
            if 'track_search' in request.form or 'artist_search' in request.form:
                track_search = request.values['track_search']
                artist_search = request.values['artist_search']

                search_results = search_tracks(artist=artist_search,
                                               name=track_search)

            # Preference Form
            if 'track_preference' in request.form:

                try:

                    track_id = request.values['track_preference']
                    other_info = find_track_info(track_id)

                    # Add Track to Database
                    new_preference = Track(id=track_id,
                                           preference=True,
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
                    print("Could not add track to database: {error}")
                    raise error
                else:
                    DB.session.commit()

        preferences = Track.query.filter(Track.preference == True).all()

        return render_template('base.html',
                               search_results=search_results,
                               preferences=preferences,
                               recommendations=recommendations)

    @app.route('/reset_preferences')
    def reset_preferences():
        '''Resets track preferences'''
        try:
            Track.query.filter(Track.preference == True).delete()
        except Exception as error:
            print(f'error deleting tracks: {error}')
            raise error
        else:
            DB.session.commit()
        return render_template('base.html',
                               search_results=None,
                               preferences=None,
                               recommendations=None)

    @app.route('/reset')
    def reset():
        '''Resets the entire database'''
        DB.drop_all()
        DB.create_all()
        return render_template('base.html',
                               search_results=None,
                               preferences=None,
                               recommendations=None)

    @app.route('/update')
    def update_tracks(search_results=None,
                      preferences=None):
        '''Updates recommendation tracks in database'''
        try:
            Track.query.filter(Track.preference == False).delete()
            # get new songs from DB
            for track in new_tracks():
                new_track = Track(id=track['id'],
                                  preference=False,
                                  name=track['name'],
                                  artists=track['artists'],
                                  danceability=track['danceability'],
                                  energy=track['energy'],
                                  key=track['key'],
                                  loudness=track['loudness'],
                                  mode=track['mode'],
                                  speechiness=track['speechiness'],
                                  acousticness=track['acousticness'],
                                  instrumentalness=track['instrumentalness'],
                                  liveness=track['liveness'],
                                  valence=track['valence'],
                                  tempo=track['tempo'],
                                  duration_ms=track['duration_ms'],
                                  time_signature=track['time_signature'])
                DB.session.add(new_track)
        except Exception as error:
            print(f'error deleting tracks: {error}')
            raise error
        else:
            DB.session.commit()
        return render_template('base.html',
                               search_results=search_results,
                               preferences=preferences,
                               recommendations=None)

    return app
