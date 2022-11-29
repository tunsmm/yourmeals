from yourmeals.recommendation.naive_recommender import NaiveRecommender
from yourmeals.recommendation.fullmeal_recommender import FullMealRecommender
from yourmeals.recommendation.lightmeal_recommender import LightMealRecommender


class RecommendationController:

    def __init__(self, n_recommendations: int) -> None:
        if n_recommendations < 2:
            raise ValueError(f"Minimal recommendation number is 2, provided {n_recommendations}.")

        self.naive = NaiveRecommender()
        self.fullmeal_preferences = FullMealRecommender(n_recommendations - 1)
        self.lightmeal_preferences = LightMealRecommender(n_recommendations - 1)

    def get_full_recommendation(self, user_email: str) -> list[str]:
        rec_list = []
        naive = self.naive.get_recommendation(user_email)
        if naive:
            rec_list.append(naive)
        preferences = self.fullmeal_preferences.get_recommendation(user_email)
        rec_list.append(*preferences)
        return rec_list

    def get_light_recommendation(self, user_email: str) -> list[str]:
        rec_list = []
        naive = self.naive.get_recommendation(user_email)
        if naive:
            rec_list.append(naive)
        preferences = self.lightmeal_preferences.get_recommendation(user_email)
        rec_list.append(*preferences)
        return rec_list
