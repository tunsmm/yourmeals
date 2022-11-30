from models.meal import Meal as Meal


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
        
        if history:
            self.history = history
        else: 
            self.history = []
        
        self.light_meals = 2
        if self.strategy == "health":
            self.full_meals = 3
        elif self.strategy == "loss":
            self.full_meals = 2
        elif self.strategy == "gain":
            self.full_meals = 4

        self.set_calories()

    def add_meal(self, meal: Meal):
        meals_per_day = sum(m.date == meal.date for m in self.history)
        if meals_per_day >= (self.full_meals + self.light_meals):
            raise ValueError(
                f"Попытка превысить количество приемов пищи в день. Сейчас - {meals_per_day}, максимум - 10."
            )
        self.history.append(meal)
    
    def get_meal(self, date):
        for meal in self.history:
            if meal.date == date:
                return meal
            
    def set_meal(self, date, new_meal: Meal):
        for meal in self.history:
            if meal.date == date:
                meal = new_meal
    
    def delete_meal(self, date):
        for index, meal in enumerate(self.history):
            if meal.date == date:
                del self.history[index]
    
    def set_calories(self):
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
