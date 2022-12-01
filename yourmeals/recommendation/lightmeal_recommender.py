from recommendation.preferences_recommender import MealPreferencesRecommender
import models as models


class LightMealRecommender(MealPreferencesRecommender):
    def __init__(self):
        super(LightMealRecommender, self).__init__()
        self.filter = lambda x: x is isinstance(x, models.meal.LightMeal) and len(x.dishes) > 0
