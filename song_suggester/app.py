from flask import Flask, render_template, request
from os import getenv
from .models import DB, Track
from .spotify import *

# pointless comment


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

                add_track_to_db(track_id=request.values['track_preference'],
                                preference=True)

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
    def update(search_results=None,
               preferences=None):
        '''Updates / Populates Tracks in Database'''

        update_tracks_in_db(num_tracks=20)

        return render_template('base.html',
                               search_results=search_results,
                               preferences=preferences,
                               recommendations=None)

    return app
