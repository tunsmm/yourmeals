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
        naive = self.naive.get_recommendation(user_email)
        preferences = self.fullmeal_preferences.get_recommendation(user_email)
        return [naive, *preferences]

    def get_light_recommendation(self, user_email: str) -> list[str]:
        naive = self.naive.get_recommendation(user_email)
        preferences = self.lightmeal_preferences.get_recommendation(user_email)
        return [naive, *preferences]
