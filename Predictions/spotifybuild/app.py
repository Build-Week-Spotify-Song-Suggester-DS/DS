from flask import Flask, render_template
import spotipy
from flask_sqlalchemy import SQLAlchemy
from os import getenv

key = getenv('CLIENT_ID')
secret = getenv('CLIENT_SECRET')

def track_search(song_or_artist):
    """hopefully finds what they're looking for"""
    search_results = [artist]
                        
    return search_results 

# construct API
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_API_URL = 'https://api.spotify.com/v1/'




urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
sp = spotipy.Spotify()
artist = sp.artist(urn)



def create_app():
    
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv(DATABASE_URI)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB= SQLAlchemy(app)

    DB.init_app(app)


    @app.route("/")
    def root():
        """base view"""
        DB.drop_all()
        DB.create_all()
        return render_template("buildproject.html", title="Song Recs")

    return app