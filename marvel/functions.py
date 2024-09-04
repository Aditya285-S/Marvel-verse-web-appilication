import os
import pickle
from django.conf import settings

similarity_path = os.path.join(settings.BASE_DIR, 'similarity.pkl')
movies_path = os.path.join(settings.BASE_DIR, 'movie_list.pkl')

movies = pickle.load(open(movies_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

def recommend(movie_name):
    try:
        index = movies[movies['Movie'] == str(movie_name)].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []

        for i in distances[1:5]:
            recommended_movie_names.append(movies.iloc[i[0]].Movie)

        return recommended_movie_names

    except IndexError:
        return []
