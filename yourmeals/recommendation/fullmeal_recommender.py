from recommendation.preferences_recommender import MealPreferencesRecommender
import models as models


class FullMealRecommender(MealPreferencesRecommender):
    def __init__(self, n_recommendations: int):
        super(FullMealRecommender, self).__init__(n_recommendations)
        self.filter = lambda x: x is models.meal.FullMeal
