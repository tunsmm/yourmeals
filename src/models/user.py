from yourmeals.src.models.base_model import BaseModel as BaseModel
from yourmeals.src.models.meal import Meal as Meal


class User(BaseModel):
    def __init__(self, email: str, name: str, 
                 weight: float, height: float, strategy: str, gender: str,
                 history: list[Meal] = None) -> None:
        self.email = email
        self.name = name
        self.weight = weight
        self.height = height
        self.strategy = strategy
        self.gender = gender
        self.history = history

    def add_meal(self, meal: Meal):
        meals_per_day = sum(m.date == meal.date for m in self.history)
        if meals_per_day >= (self.full_meals + self.light_meals):
            raise ValueError(
                f"Попытка превысить количество приемов пищи в день. Сейчас - {meals_per_day}, максимум - 10."
            )
        self.get_history().append(meal)
    
    def get_history(self):
        if not self.history:
            self.history = list()
        return self.history
    
    def set_full_meals(self):
        if self.strategy == "health":
            self.full_meals = 3
        elif self.strategy == "loss":
            self.full_meals = 2
        elif self.strategy == "gain":
            self.full_meals = 4
    
    def get_full_meals(self):
        return self.full_meals
    
    def set_light_meals(self):
        self.light_meals = 2
    
    def get_light_meals(self):
        return self.light_meals
    
    def set_calories(self):
        gender_factor = self._get_gender_factor(self.gender)
        strategy_factor = self._get_strategy_factor(self.strategy)
        self.calories = (10 * self.weight + 6.25 * self.height - 4.92 * self.age + gender_factor) * strategy_factor
    
    def get_calories(self):
        return self.calories
    
    def _get_gender_factor(self, gender: str) -> int:
        if gender == "man":
            return 5
        elif gender == "woman":
            return -161
        else:
            raise ValueError(f"Unexpected gender - {gender}")
    
    def _get_strategy_factor(self, strategy: str) -> int:
        if strategy == "health":
            return 1.2
        elif strategy == "loss":
            return 0.95
        elif strategy == "gain":
            return 1.6
        else: 
            raise ValueError(f"Unexpected strategy - {strategy}")
