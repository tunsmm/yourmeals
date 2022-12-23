from operator import attrgetter

from yourmeals.data_access.data_access_module import DataAccessModule as DAM


class NaiveRecommender:
    def __init__(self):
        self.dam = DAM()

    def get_recommendation(self, user_email):
        user = self.dam.get_user(user_email)
        history = user.history
        meals = list(filter(lambda meal: len(meal.dishes) > 0, history))
        if len(history) <= 1:
            return None
        last_meal = max(meals, key=attrgetter('date'))
        dish = max(last_meal.dishes, key=attrgetter('calories'))
        return dish.name
