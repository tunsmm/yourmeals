from yourmeals.recommendation.preferences_recommender import MealPreferencesRecommender
import yourmeals.models as models


class LightMealRecommender(MealPreferencesRecommender):
    def __init__(self, n_recommendations: int):
        super(LightMealRecommender, self).__init__(n_recommendations)
        self.filter = lambda x: x is models.meal.LightMeal
