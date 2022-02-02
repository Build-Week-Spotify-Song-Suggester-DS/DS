from Models import models
from sklearn.linear_model import LogisticRegression
import numpy as np



def recommend_songs(rec_tracks, hypo_music):
    '''
    determine and returns which songs are most similiar to the given song.
    '''

    # Query for the recommended songs 
    given_song = models.Track.query.filter(models.Track.preference == True).all()
    rec_songs = models.Track.query.filter(models.Track.track == rec_tracks).all()

    # get word embeddings of the songs for both given song and rec songs
    given_song_vects = np.array([models.Track.vect for track in given_song])
    rec_songs_vects = np.array([models.Track.vect for track in rec_songs])

    # combine two word embeddings into one big 2D numpy array
    vects = np.vstack([given_song_vects, rec_songs_vects])


    # create a np array to represent the y vector 
    labels = np.concatenate([np.zeros(len(given_song)),
                             np.ones(len(rec_songs))])
    

    #import and train our logisitic regression
    log_reg = LogisticRegression()

    # train out logisitic regression
    log_reg.fit(vects, labels)

    # get the word emebeddings for our hypo_music
    hypo_music_vect = np.vectorize(hypo_music)

    # generate a prediction
    prediction = log_reg.predict([hypo_music_vect])

    return prediction[0] 


