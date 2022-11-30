from data_access.data_access_module import DataAccessModule as DAM
from models.meal import get_meal
import models as models
import utils as utils

from operator import attrgetter


class NaiveRecommender:
    def __init__(self):
        self.dam = DAM()

    def get_recommendation(self, user_email):
        user = self.dam.get_user(user_email)
        history = user.history
        if len(history) <= 1:
            return None
        last_meal = max(history, key=attrgetter('date'))
        dish = max(last_meal.dishes, key=attrgetter('calories'))
        return dish.name
