from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Track(DB.Model):

    # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features

    id = DB.Column(DB.String, primary_key=True, nullable=False)

    preference = DB.Column(DB.Boolean, nullable=False)

    name = DB.Column(DB.String)

    artists = DB.Column(DB.String)

    acousticness = DB.Column(DB.Float)

    danceability = DB.Column(DB.Float)

    duration_ms = DB.Column(DB.Integer)

    energy = DB.Column(DB.Float)

    instrumentalness = DB.Column(DB.Float)

    key = DB.Column(DB.Integer)

    liveness = DB.Column(DB.Float)

    loudness = DB.Column(DB.Float)

    mode = DB.Column(DB.Integer)

    speechiness = DB.Column(DB.Float)

    tempo = DB.Column(DB.Float)

    time_signature = DB.Column(DB.Integer)

    valence = DB.Column(DB.Float)

    def __repr__(self):
        return f'{self.name} - {self.artists}'
