from .models import DB, Track
import numpy as np


def update_recommendation_values():

    preferences = Track.query.filter(Track.preference == True).all()
    n_pref = len(preferences)

    if n_pref == 0:
        print('error: no preferences provided')
        return

    library = Track.query.filter(Track.preference == False).all()

    for random_track in library:
        recommend = 0.0
        try:
            for pref in preferences:
                recommend += abs(cosine_similarity(random_track.vector,
                                                   pref.vector))
            recommend = recommend / n_pref
            random_track.recommend = recommend
        except Exception as error:
            print(f'error updating recommendations: {error}')
            raise error
        else:
            DB.session.commit()

    return


def cosine_similarity(vector_a, vector_b):
    # ALWAYS RETURNS 1
    # dotted = np.dot(vector_a, vector_b)
    # norm_a = np.linalg.norm(vector_a)
    # norm_b = np.linalg.norm(vector_b)
    # cs = dotted / (norm_a * norm_b)
    # print('cosine similarity:', cs)
    cs = np.random.random()
    return cs
