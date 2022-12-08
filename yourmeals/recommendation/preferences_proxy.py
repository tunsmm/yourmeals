from yourmeals.recommendation.lightmeal_recommender import LightMealRecommender
from yourmeals.recommendation.fullmeal_recommender import FullMealRecommender


class MealPreferencesRecommenderProxy:
    def __init__(self, meal_type: str):
        if meal_type == 'light':
            self.recommender = LightMealRecommender()
        elif meal_type == 'full':
            self.recommender = FullMealRecommender()
        else:
            raise ValueError(f"Неизвестный тип блюда - {meal_type}")

    def get_recommendation(self, user_email, n_recommendations) -> list[str]:
        recommendation = self.recommender.get_recommendation(user_email, n_recommendations)
        return recommendation
