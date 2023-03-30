from yourmeals.recommendation.preferences_recommender import MealPreferencesRecommender
import yourmeals.data_access.model as models


class LightMealRecommender(MealPreferencesRecommender):
    def __init__(self):
        super(LightMealRecommender, self).__init__()

    def filter_meals(self, history):
        filter_l = lambda x: x is isinstance(x, models.meal.LightMeal) and len(x.dishes) > 0
        filtered = list(filter(filter_l, history))
        return filtered
