from yourmeals.src.data_access.dish import Meal


class User:
    def __init__(self, email: str, name: str, full_meals: int, light_meals: int, 
                 weight: float, height: float, calories: float, history: list[Meal]) -> None:
        self.email = email
        self.name = name
        self.full_meals = full_meals
        self.light_meals = light_meals
        self.weight = weight
        self.height = height
        self.calories = calories
        self.history = history
    
    def add_meal(self, meal: Meal):
        meal_day = sum(m.date == meal.date for m in self.history)
        if meal_day >= 10:
            raise ValueError(
                f"Попытка превысить количество приемов пищи в день. Сейчас - {meal_day}, максимум - 10."
            )
        self.history.append(meal)
