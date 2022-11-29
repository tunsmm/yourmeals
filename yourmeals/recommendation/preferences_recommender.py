from data_access.data_access_module import DataAccessModule as DAM
from models.meal import get_meal
import models as models
import utils as utils
from . import text2vec

from operator import attrgetter
import numpy as np
from sklearn.neighbors import NearestNeighbors


class MealPreferencesRecommender:
    def __init__(self, n_recommendations: int):
        self.n_recommendations = n_recommendations

        self.dam = DAM()
        self.filter = None
        dish_to_recipe = self.dam.get_name_recipes()
        vectorizer = text2vec.text2vec(list(dish_to_recipe.values()))
        self.vectors = vectorizer.tfidf_weighted_wv()
        self.vector_to_name = dict(zip(self.vectors, list(dish_to_recipe.keys())))
        self.name_to_vector = dict(zip((dish_to_recipe.keys()), self.vectors))

        self.nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(self.vectors)

    def get_recommendation(self, user_email) -> list[str]:
        user = self.dam.get_user(user_email)
        history = user.history
        meals = list(filter(self.filter, history))

        if len(meals) > 1:
            main_dishes = [max(meal.dishes, key=attrgetter('calories')) for meal in meals]
            dish_vectors = np.array([self.get_dish_vector(dish) for dish in main_dishes])
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
        nearest_vectors = self.vectors[indices]
        recommended_dishes = [self.vector_to_name[vector] for vector in nearest_vectors]
        return recommended_dishes

    def get_dish_vector(self, dish: models.dish.Dish):
        return self.name_to_vector[dish.name]
