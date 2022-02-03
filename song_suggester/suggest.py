from .models import DB, Track
import numpy as np
import pandas as pd


def update_recommendation_values():

    pref_vectors = Track.query.filter(
        Track.preference == True).with_entities(Track.vector).all()

    library_vectors = Track.query.filter(
        Track.preference == False).with_entities(Track.vector).all()

    for i, library_vector in enumerate(library_vectors):
        recommend = 0.0
        for pref_vector in pref_vectors:
            recommend += abs(cosine_similarity(library_vector,
                                               pref_vector))
        recommend = recommend / len(pref_vectors)

        if i == 0:
            recommendations = {'library_offset': [i],
                               'recommendation_value': [recommend]}
        else:
            recommendations['library_offset'].append(i)
            recommendations['recommendation_value'].append(recommend)

    recommendations_df = pd.DataFrame(
        recommendations).sort_values(by='recommendation_value')

    for _, row in recommendations_df.iterrows():
        Track.query.filter(Track.preference == False).offset(
            row['library_offset']).first().recommend = row['recommendation_value']

    return


def cosine_similarity(vector_a, vector_b):
    # ALWAYS RETURNS 1
    # dot = np.dot(vector_a, vector_b)
    # norm_a = np.linalg.norm(vector_a)
    # norm_b = np.linalg.norm(vector_b)
    # cs = dot / (norm_a * norm_b)
    # print('cosine similarity 1:', cs)

    cs = np.random.random()
    # print('cosine similarity:', cs)

    return cs
