from data_access.data_access_module import DataAccessModule as DAM
from models.meal import get_meal
import models as models
import utils as utils
from . import text2vec

from operator import attrgetter
import numpy as np
from sklearn.neighbors import NearestNeighbors

from os.path import exists


class MealPreferencesRecommender:
    def __init__(self, n_recommendations: int):
        self.n_recommendations = n_recommendations

        self.dam = DAM()
        self.filter = None
        self.dish_to_recipe = self.dam.get_name_recipes()

        if exists('vectors.npy'):
            self.vectors = np.load('vectors.npy', allow_pickle=True)
        else:
            self.vectors = self.get_all_vectors()
            np.save('vectors.npy', self.vectors)
        self.vector_index_to_name = dict(zip(range(len(self.vectors)), list(self.dish_to_recipe.keys())))
        self.name_to_index = dict(zip((self.dish_to_recipe.keys()), range(len(self.vectors))))

        self.nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(self.vectors)

    def get_all_vectors(self):
        vectorizer = text2vec.text2vec(list(self.dish_to_recipe.values()))
        vectors = vectorizer.tfidf_weighted_wv()
        return vectors

    def get_recommendation(self, user_email) -> list[str]:
        user = self.dam.get_user(user_email)
        history = user.history
        meals = list(filter(self.filter, history))

        if len(meals) > 1:
            main_dishes = [max(meal.dishes, key=attrgetter('calories')) for meal in meals]
            dish_vectors = np.array([self.vectors[self.get_dish_vector(dish)] for dish in main_dishes])
            mean = dish_vectors.mean(axis=0)
            std = dish_vectors.mean(axis=0)
        else:
            mean = self.vectors.mean(axis=0)
            std = self.vectors.std(axis=0)

        random_samples = []
        for i in range(self.n_recommendations):
            sample = mean + np.random.normal(0, std, size=(300,)).astype('float32')
            random_samples.append(sample)
        random_samples = np.array(random_samples)

        distances, indices = self.nbrs.kneighbors(random_samples)
        # nearest_vectors = self.vectors[indices]
        recommended_dishes = [self.vector_index_to_name[index] for index in indices]
        return recommended_dishes

    def get_dish_vector(self, dish: models.dish.Dish):
        return self.name_to_index[dish.name]
