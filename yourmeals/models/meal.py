import datetime

from yourmeals.models.dish import Dish as Dish


class Meal:
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now().date(), time=datetime.datetime.now().time()) -> None:
        if not dishes:
            dishes = []
        self.dishes = dishes
        self.date = date
        self.time = time
        self.sum_calories = self.calculate_sum_calories()
        self.limit_calories = 3000
    
    def __str__(self):
        return f"Прием пищи за {str(self.date)} {str(self.time)}"
    
    def get_dish(self, dish_name: str) -> Dish:
        for dish in self.dishes:
            if dish.name == dish_name:
                return dish
    
    def delete_dish(self, dish_name: str) -> None:
        for index, dish in enumerate(self.dishes):
            if dish.name == dish_name:
                del self.dishes[index]
    
    def calculate_sum_calories(self) -> int: 
        return sum(dish.calories_on_portion for dish in self.dishes)
    
    def add_dish(self, dish: Dish) -> None:
        if self.sum_calories + dish.calories_on_portion > self.limit_calories:
            raise ValueError(
                f"В приеме пищи не может быть больше {self.limit_calories} калорий. \
                Сейчас калорий: {self.sum_calories}, в добавляемом блюде - {dish.calories_on_portion}"
            )
        self.dishes.append(dish)
        self.sum_calories += dish.calories_on_portion


class FullMeal(Meal):
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now) -> None:
        super().__init__(dishes, date)
        self.meal_type = 'full'
        self.limit_calories = 1500


class LightMeal(Meal):
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now) -> None:
        super().__init__(dishes, date)
        self.meal_type = 'light'
        self.limit_calories = 500


def get_meal(meal_type: str) -> Meal:
    if meal_type == 'light':
        return LightMeal()
    elif meal_type == 'full':
        return FullMeal()
    else:
        raise ValueError(f"Неизвестный тип блюда - {meal_type}")


def get_type(meal) -> Meal:
    if isinstance(meal, LightMeal):
        return 'light'
    elif isinstance(meal, FullMeal):
        return 'full'
    else:
        raise ValueError(f"Неизвестный тип блюда - {meal}")
