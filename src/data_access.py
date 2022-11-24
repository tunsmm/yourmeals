import datetime


class Dish:
    def __init__(self, name: str, calories: float, proteins: float, fats: float, carbohydrates: float, 
                 recipe: str, description: str, preparing_time: str, ingredients: list[dict], 
                 portions: int, tags: list, img_src: str) -> None:
        self.name = name
        self.calories = calories
        self.proteins = proteins
        self.fats = fats
        self.carbohydrates = carbohydrates
        self.recipe = recipe
        self.description = description
        self.ingredients = ingredients
        self.portions = portions
        self.tags = tags
        self.img_src = img_src
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Dish):
            raise TypeError("Операнд справа должен иметь тип Dish")
        return self.name == __o.name and self.ingredients == __o.ingredients and self.recipe == __o.recipe
    
    def __str__(self) -> str:
        return self.name


class MealFactory:
    def get_meal_type(self, meal_type: str):
        if meal_type == 'Light':
            return LightMeal
        elif meal_type == 'Full':
            return FullMeal
        else:
            raise ValueError(f"Неизвестный тип блюда - {meal_type}")


class Meal:
    def __init__(self, dishes: list[Dish] = None, date=datetime.datetime.now) -> None:
        self.dishes = dishes
        self.date = date
    
    def __str__(self):
        return f"Прием пищи за {str(self.date)}"
    
    def add_dish(self, dish: Dish):
        sum_calories = sum(d.calories for d in self.dishes)
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
        sum_calories = sum(d.calories for d in self.dishes)
        if sum_calories + dish.calories > 500:
            raise ValueError(
                f"В перекусе не может быть больше 500 калорий. \
                Сейчас калорий -{sum_calories}, в добавляемом блюде - {dish.calories}"
            )
        self.dishes.append(dish)


class UserHistory:
    def __init__(self, history: list[Meal]) -> None:
        self.history = history
    
    def add_meal(self, meal: Meal):
        meal_day = sum(m.date == meal.date for m in self.history)
        if meal_day >= 10:
            raise ValueError(
                f"Попытка превысить количество приемов пищи в день. Сейчас - {meal_day}, максимум - 10."
            )
        self.history.append(meal)


class User:
    def __init__(self, email: str, name: str, full_meals: int, light_meals: int, 
                 weight: float, height: float, calories: float, history: UserHistory) -> None:
        self.email = email
        self.name = name
        self.full_meals = full_meals
        self.light_meals = light_meals
        self.weight = weight
        self.height = height
        self.calories = calories
        self.history = history
    
    def add_meal(self, meal: Meal):
        self.history.add_meal(meal)
