from itertools import chain
from operator import attrgetter

from yourmeals.data_access.data_access_module import DataAccessModule as DAM


class NaiveRecommender:
    def __init__(self):
        self.dam = DAM()

    def get_recommendation(self, user_email):
        user = self.dam.get_user(user_email, add_history=True)
        history = user.history
        if not history:
            return None
        
        last_meals = list()
        for meals in history.values():
            last_meals.extend(meals[::-1])
            if any([bool(meal.dishes) for meal in meals[::-1]]):
                break
        
        last_dishes = list()
        for meal in last_meals:
            if meal.dishes:
                last_dishes.extend(meal.dishes[::-1])
                break
        if not last_dishes:
            return None
        
        dish = max(last_dishes, key=attrgetter('calories'))
        return dish.name
