from recommendation.naive_recommender import NaiveRecommender
from recommendation.fullmeal_recommender import FullMealRecommender
from recommendation.lightmeal_recommender import LightMealRecommender
from recommendation.preferences_recommender import MealPreferencesRecommender


class RecommendationController:

    def __init__(self, n_recommendations: int) -> None:
        if n_recommendations < 2:
            raise ValueError(f"Minimal recommendation number is 2, provided {n_recommendations}.")

        self.naive = NaiveRecommender()
        self.fullmeal_preferences = FullMealRecommender()
        self.lightmeal_preferences = LightMealRecommender()
        self.n_recommendations = n_recommendations

    def get_full_recommendation(self, user_email: str) -> list[str]:
        rec_list = self.get_recommendation(user_email, self.fullmeal_preferences)
        return rec_list

    def get_light_recommendation(self, user_email: str) -> list[str]:
        rec_list = self.get_recommendation(user_email, self.lightmeal_preferences)
        return rec_list

    def get_recommendation(self, user_email, recommender: MealPreferencesRecommender):
        rec_list = []
        naive = self.naive.get_recommendation(user_email)
        if naive:
            rec_list.append(naive)
        preferences = recommender.get_recommendation(user_email, self.n_recommendations - len(rec_list))
        rec_list += preferences
        return rec_list
