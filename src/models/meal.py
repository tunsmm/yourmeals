import datetime

from yourmeals.src.models.dish import Dish as Dish


class Meal:
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now) -> None:
        self.dishes = dishes
        self.date = date
    
    def __str__(self):
        return f"Прием пищи за {str(self.date)}"
    
    def get_dish(self, dish: str) -> Dish:
        for dish in self.dishes:
            if dish.name == dish:
                return dish
    
    def sum_calories(self): 
        return sum(d.calories for d in self.dishes)
    
    def set_date(self, date):
        self.date = date
    
    def add_dish(self, dish: Dish):
        sum_calories = self.sum_calories()
        if sum_calories + dish.calories > 5000:
            raise ValueError(
                f"В приеме пищи не может быть больше 5000 калорий. \
                Сейчас калорий -{sum_calories}, в добавляемом блюде - {dish.calories}"
            )
        self.dishes.append(dish)


class FullMeal(Meal):
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now) -> None:
        super().__init__(dishes, date)


class LightMeal(Meal):
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now) -> None:
        super().__init__(dishes, date)

    def add_dish(self, dish: Dish):
        sum_calories = self.sum_calories()
        if sum_calories + dish.calories > 500:
            raise ValueError(
                f"В перекусе не может быть больше 500 калорий. \
                Сейчас калорий -{sum_calories}, в добавляемом блюде - {dish.calories}"
            )
        self.dishes.append(dish)


def get_meal(self, meal_type: str) -> Meal:
    if meal_type == 'Light':
        return LightMeal()
    elif meal_type == 'Full':
        return FullMeal()
    else:
        raise ValueError(f"Неизвестный тип блюда - {meal_type}")
