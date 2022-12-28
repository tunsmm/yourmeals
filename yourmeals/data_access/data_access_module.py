from itertools import chain
import datetime

from mongoengine.errors import DoesNotExist

from yourmeals.diaryapp import models as orm
from yourmeals.models.dish import Dish as Dish
from yourmeals.models.meal import get_type, get_meal
from yourmeals.models.user import User as User


class DataAccessModule:
    def save_user(self, user: User):
        orm_user = orm.User(
            email=user.email,
            name=user.name,
            age=user.age,
            weight=user.weight,
            height=user.height,
            gender=user.gender,
            strategy=user.strategy,
            full_meals=user.full_meals,
            light_meals=user.light_meals,
            calories=user.calories,
            history=user.history,
        )
        orm_user.save()
    
    def update_user(self, user: User):
        orm_user = orm.User.objects.get(email=user.email)
        orm_user.email = user.email
        orm_user.name = user.name
        orm_user.age = user.age
        orm_user.weight = user.weight
        orm_user.height = user.height
        orm_user.gender = user.gender
        orm_user.strategy = user.strategy
        orm_user.full_meals = user.full_meals
        orm_user.light_meals = user.light_meals
        orm_user.calories = user.calories
        
        meals = []
        for meal in chain(*user.history.values()):
            dishes = [dish.name for dish in meal.dishes]
            date_time = datetime.datetime.combine(meal.date, meal.time)
            meals.append(orm.Meal(
                meal_type=get_type(meal),
                date=date_time,
                dishes=dishes,
            ))
        orm_user.history = meals
        
        orm_user.save()
        
    def get_user(self, email: str, add_history: bool = False) -> User:
        try:
            orm_user = orm.User.objects.get(email=email)
        except DoesNotExist:
            return None
        user = User(
            email=orm_user.email,
            name=orm_user.name,
            age=orm_user.age,
            weight=orm_user.weight,
            height=orm_user.height,
            gender=orm_user.gender,
            strategy=orm_user.strategy,
        )
        if add_history and orm_user.history:
            for orm_meal in orm_user.history:
                meal = get_meal(orm_meal.meal_type)
                meal.date = orm_meal.date.date()
                meal.time = orm_meal.date.time()
                for dish_name in orm_meal.dishes:
                    meal.add_dish(self.get_dish(dish_name))
                user.add_meal(meal)
        return user

    def get_dishes_names(self, dish_name: str) -> list[str]:
        orm_dishes = orm.Dish.objects(name__icontains=dish_name)
        return [
            orm_dish.name
            for orm_dish in orm_dishes
        ]

    def get_dish(self, dish_name: str) -> Dish:
        orm_dish = orm.Dish.objects(name__contains=dish_name)[0]
        return Dish(
            name=orm_dish.name,
            calories=orm_dish.calories,
            proteins=orm_dish.proteins,
            fats=orm_dish.fats,
            carbohydrates=orm_dish.carbohydates,
            recipe=orm_dish.recipe,
            description=orm_dish.description,
            preparing_time=orm_dish.preparing_time,
            ingredients=orm_dish.ingredients,
            portions=orm_dish.portions,
            tags=orm_dish.tags,
            img_src=orm_dish.img_src,
        )

    # Fix. Concatenate in one function
    def get_name_recipes(self) -> dict[str, str]:
        names = orm.Dish.objects.values_list('name')
        recipes = orm.Dish.objects.values_list('recipe')
        recipes = [' '.join(recipe) for recipe in recipes]
        name_recipe_dict = dict(zip(names, recipes))
        return name_recipe_dict
