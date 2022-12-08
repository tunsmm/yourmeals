from yourmeals.recommendation.preferences_recommender import MealPreferencesRecommender
import yourmeals.models as models


class FullMealRecommender(MealPreferencesRecommender):
    def __init__(self):
        super(FullMealRecommender, self).__init__()

    def filter_meals(self, history):
        filter_l = lambda x: isinstance(x, models.meal.FullMeal) and len(x.dishes) > 0
        filtered = list(filter(filter_l, history))
        return filtered
