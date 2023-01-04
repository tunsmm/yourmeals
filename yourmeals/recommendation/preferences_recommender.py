from operator import attrgetter

from sklearn.neighbors import NearestNeighbors
import numpy as np

from . import text2vec
from yourmeals.data_access.data_access_module import DataAccessModule as DAM
import yourmeals.models as models
import yourmeals.utils as utils


class MealPreferencesRecommender:
    def __init__(self):
        self.dam = DAM()
        self.dish_to_recipe = self.dam.get_name_recipes() # Return all dishes
        self.vectors = self.get_all_vectors() # All dishes to vectors

        self.vector_index_to_name = dict(zip(range(len(self.vectors)), list(self.dish_to_recipe.keys())))
        self.name_to_index = dict(zip((self.dish_to_recipe.keys()), range(len(self.vectors))))

        self.nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(self.vectors)

    @utils.numpy_cache
    def get_all_vectors(self):
        vectorizer = text2vec.text2vec(list(self.dish_to_recipe.values()))
        vectors = vectorizer.tfidf_weighted_wv()
        return vectors

    def filter_meals(self, history):
        filter_l = lambda x: len(x.dishes) > 0
        filtered = list(filter(filter_l, history))
        return filtered

    def get_user_preferences(self, meals):
        if len(meals) > 1:
            main_dishes = [max(meal.dishes, key=attrgetter('calories')) for meal in meals]
            dish_vectors = np.array([self.vectors[self.get_dish_vector(dish)] for dish in main_dishes])
            mean = dish_vectors.mean(axis=0)
            std = dish_vectors.std(axis=0)
        else:
            mean = self.vectors.mean(axis=0)
            std = self.vectors.std(axis=0)
        return mean, std

    def get_recommended_vectors(self, mean, std, n_recommendations):
        random_samples = []
        for i in range(n_recommendations):
            sample = mean + np.random.normal(0, std * 3, size=(300,)).astype('float32')
            random_samples.append(sample)
        random_samples = np.array(random_samples)
        return random_samples

    def get_recommendation(self, user_email, n_recommendations) -> list[str]:
        user = self.dam.get_user(user_email, add_history=True)
        history = user.history
        meals = self.filter_meals(history)
        np.random.seed(len(meals) + hash(user_email) % 10000)
        mean, std = self.get_user_preferences(meals)
        random_samples = self.get_recommended_vectors(mean, std, n_recommendations)
        distances, indices = self.nbrs.kneighbors(random_samples)
        recommended_dishes = [self.vector_index_to_name[index] for index in indices.flatten()]
        return recommended_dishes

    def get_dish_vector(self, dish: models.dish.Dish):
        return self.name_to_index[dish.name]
