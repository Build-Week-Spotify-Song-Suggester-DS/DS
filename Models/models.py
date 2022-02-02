from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Characteristics(DB.Model):
    '''displays characteristics of a track'''
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    acousticness = DB.Column(DB.Float, nullable=False)
    danceability = DB.Column(DB.Float, nullable=False)
    energy = DB.Column(DB.Float, nullable=False)
    instrumentalness = DB.Column(DB.Float, nullable=False)
    duration_ms = DB.Column(DB.Integer, nullable=False)
    key = DB.Column(DB.Integer, nullable=False)
    liveness = DB.Column(DB.Float, nullable=False)
    loudness = DB.Column(DB.Float, nullable=False)
    mode = DB.Column(DB.Integer, nullable=False)
    speechiness = DB.Column(DB.Float, nullable=False)
    tempo = DB.Column(DB.Float, nullable=False)
    time_signature = DB.Column(DB.Float, nullable=False)
    valence = DB.Column(DB.Float, nullable=False)


class Artist(DB.Model):
    '''displays artist'''
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    artist = DB.Column(DB.String, nullable=False)


class Track(DB.Model):
    '''displays track'''
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    track = DB.Column(DB.String, nullable=False)
    artist_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'artist.id'), nullable=False)
    artist = DB.relationship("Artist", backref=DB.backref('tracks'), lazy=True)

    vect = DB.Column(DB.PickleType, nullable=False)




