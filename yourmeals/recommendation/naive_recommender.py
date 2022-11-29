from yourmeals.data_access.data_access_module import DataAccessModule as DAM
from yourmeals.models.meal import get_meal
import yourmeals.models as models
import yourmeals.utils as utils

from operator import attrgetter


class NaiveRecommender:
    def __init__(self):
        self.dam = DAM()

    def get_recommendation(self, user_email):
        user = self.dam.get_user(user_email)
        history = user.history
        if len(history) == 0:
            return None
        last_meal = max(history, key=attrgetter('date'))
        dish = max(last_meal.dishes, key=attrgetter('calories'))
        return dish.name
