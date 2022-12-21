from yourmeals.recommendation.naive_recommender import NaiveRecommender
from yourmeals.recommendation.preferences_proxy import MealPreferencesRecommenderProxy

from yourmeals.utils import Singleton


class RecommendationController(metaclass=Singleton):

    def __init__(self, n_recommendations: int) -> None:
        if n_recommendations < 2:
            raise ValueError(f"Minimal recommendation number is 2, provided {n_recommendations}.")

        self.naive = NaiveRecommender()
        self.fullmeal_preferences = MealPreferencesRecommenderProxy('full')
        self.lightmeal_preferences = MealPreferencesRecommenderProxy('light')
        self.n_recommendations = n_recommendations

    def get_full_recommendation(self, user_email: str) -> list[str]:
        rec_list = self.get_recommendation(user_email, self.fullmeal_preferences)
        return rec_list

    def get_light_recommendation(self, user_email: str) -> list[str]:
        rec_list = self.get_recommendation(user_email, self.lightmeal_preferences)
        return rec_list

    def get_recommendation(self, user_email, recommender: MealPreferencesRecommenderProxy):
        rec_list = []
        naive = self.naive.get_recommendation(user_email)
        if naive:
            rec_list.append(naive)
        preferences = recommender.get_recommendation(user_email, self.n_recommendations - len(rec_list))
        rec_list += preferences
        return rec_list
