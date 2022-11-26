from yourmeals.src.data_access.data_access_module import DataAccessModule as DAM
from yourmeals.src.models.meal import get_meal
import yourmeals.src.models as models
import utils

from operator import attrgetter


class RecommendationController:

    def __init__(self) -> None:
        self.dam = DAM()

    def get_recommendation(self, user_email: str) -> list(str):
        naive = self.naive_rec(user_email)
        return [naive]

    # TODO: naive recommendation to separate recommender

    def naive_rec(self, user_email):
        user = self.dam.get_user(user_email)
        history = user.history
        last_meal = max(history, key=attrgetter('date'))
        dish = max(last_meal.dishes, key=attrgetter('calories'))
        return dish.name
