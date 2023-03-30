import datetime

from .meal import Meal as Meal


class User:
    def __init__(self, email: str, name: str, age: int, 
                 weight: float, height: float, strategy: str, gender: str,
                 history: list[Meal] = None, ) -> None:
        self.email = email
        self.name = name
        self.weight = weight
        self.height = height
        self.strategy = strategy
        self.gender = gender
        self.age = age
        
        self.history = {}
        
        self.light_meals = 2
        if self.strategy == "health":
            self.full_meals = 3
        elif self.strategy == "loss":
            self.full_meals = 2
        elif self.strategy == "gain":
            self.full_meals = 4

        self.set_calories()

    def add_meal(self, meal: Meal):
        meal_type = meal.meal_type
        if meal_type == 'light':
            limit = self.light_meals
        elif meal_type == 'full':
            limit = self.full_meals
        else:
            raise ValueError(f"Unexpected type {meal_type}")
            
        meals_per_day = sum(meal_type == m.meal_type for m in self.history.setdefault(str(meal.date), []))
        if meals_per_day >= limit:
            raise ValueError(
                f"Вы превышаете максимальное количество приемов пищи в день."
            )
        self.history[str(meal.date)].append(meal)
    
    def get_meal(self, date: datetime.date, time: datetime.time) -> Meal:
        for meal in self.history[str(date)]:
            if meal.time == time:
                return meal
            
    def set_meal(self, date: datetime.date, time: datetime.time, new_meal: Meal) -> None:
        for i, meal in enumerate(self.history[str(date)]):
            if meal.time == time:
                self.history[str(date)] = new_meal
    
    def delete_meal(self, date: datetime.date, time: datetime.time) -> None:
        for index, meal in enumerate(self.history[str(date)]):
            if meal.time == time:
                del self.history[str(date)][index]
    
    def set_calories(self) -> None:
        gender_factor = self._get_gender_factor(self.gender)
        strategy_factor = self._get_strategy_factor(self.strategy)
        self.calories = round(
            (10 * self.weight + 6.25 * self.height - 4.92 * self.age + gender_factor) * strategy_factor
        )
    
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
