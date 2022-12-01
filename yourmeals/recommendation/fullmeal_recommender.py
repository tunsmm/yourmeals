from recommendation.preferences_recommender import MealPreferencesRecommender
import models as models


class FullMealRecommender(MealPreferencesRecommender):
    def __init__(self):
        super(FullMealRecommender, self).__init__()
        self.filter = lambda x: isinstance(x, models.meal.FullMeal) and len(x.dishes) > 0
