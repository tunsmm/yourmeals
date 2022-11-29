from models.dish import Dish as Dish
from models.user import User as User

import diaryapp.models as orm


class DataAccessModule:
    """
    у тебя должны быть те классы из mongoengine
    и к ним ты пишешь модуль, в котором mongoengine классы преобразуются в классы, которые ты сегодня написал
    т. е. у него есть методы create user, add meal to user, add dish to meal
    и наоборот
    get user, get meal, get dish

    """
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
        
    def get_user(self, email: str) -> User:
        orm_user = orm.User.objects.get(email=email)
        return User(
            email=orm_user.email,
            name=orm_user.name,
            age=orm_user.age,
            weight=orm_user.weight,
            height=orm_user.height,
            history=orm_user.history,
            gender=orm_user.gender,
            strategy=orm_user.strategy,
        )

    def get_dish(self, dish_name: str) -> Dish:
        orm_dish = orm.Dish.objects(name__icontains=dish_name)
        return Dish(
            name=orm_dish.name,
            calories=orm_dish.calories,
            proteins=orm_dish.proteins,
            fats=orm_dish.fats,
            carbohydrates=orm_dish.carbohydates,
            recipe=orm_dish.recipe,
            description=orm_dish.description,
            preparing_time=orm_dish.preparing_time(),
            ingredients=orm_dish.ingredients,
            portions=orm_dish.portions,
            tags=orm_dish.tags,
            img_src=orm_dish.img_src,
        )

    def get_name_recipes(self) -> dict[str, str]:
        names = Dish.objects.values_list('name')
        recipes = orm.Dish.objects.values_list('recipe')
        recipes = [' '.join(recipe) for recipe in recipes]
        name_recipe_dict = dict(zip(names, recipes))
        return name_recipe_dict
