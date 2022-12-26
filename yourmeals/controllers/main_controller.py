import datetime

from yourmeals.data_access.data_access_module import DataAccessModule as DAM
from yourmeals.models.meal import get_meal
from yourmeals.controllers.recommendation_controller import RecommendationController
import yourmeals.models as models
import yourmeals.utils as utils


class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class MainController(metaclass=Singleton):
    def __init__(self) -> None:
        self.dam = DAM()
        self.recommender = RecommendationController(3)
        
    def create_user(self, email: str, name: str, age: int, weight: float, height: float, strategy: str, gender: str,):
        user = models.user.User(
            email=email,
            name=name,
            age=age,
            weight=weight,
            height=height,
            gender=gender,
            strategy=strategy,
        )
        self.dam.save_user(user)
        
    def update_user(self, email: str, name: str, age: int, weight: float, height: float, strategy: str, gender: str):
        user = self.dam.get_user(email=email)
        user.name = name
        user.age = age
        user.weight = weight
        user.height = height
        user.strategy = strategy
        user.gender = gender
        self.dam.update_user(user)
    
    def add_meal_to_user(self, email: str, meal_type: str, date: datetime.datetime, ):
        user = self.dam.get_user(email=email, add_history=True)
        meal = get_meal(meal_type)
        meal.date = date.date()
        meal.time = date.time()
        user.add_meal(meal)
        self.dam.update_user(user)
        
    def delete_meal(self, email: str, date: dict, time: dict):
        user = self.dam.get_user(email=email, add_history=True)
        user.delete_meal(
            utils.dict_to_date(date), 
            utils.dict_to_time(time)
        )
        self.dam.update_user(user)
        
    def add_dish_to_meal(self, email: str, date: dict, time: dict, dishes: list[str]):
        user = self.dam.get_user(email=email, add_history=True)
        date = utils.dict_to_date(date)
        time = utils.dict_to_time(time)
        meal = user.get_meal(date, time)
        for dish_name in dishes:
            dish = self.dam.get_dish(dish_name=dish_name)
            meal.add_dish(dish)
        user.set_meal(date, time, meal)
        self.dam.update_user(user)

    def delete_dish_on_meal(self, email: str, date: dict, time: dict, dish_name: str):
        user = self.dam.get_user(email=email, add_history=True)
        meal = user.get_meal(
            utils.dict_to_date(date),
            utils.dict_to_time(time)
        )
        meal.delete_dish(dish_name)
        self.dam.update_user(user)
    
    def get_dish(self, dish_name: str) -> str:
        dish = self.dam.get_dish(dish_name=dish_name)
        return utils.toJSON(dish)
    
    def get_dishes_names(self, dish_name: str) -> str:
        dishes = self.dam.get_dishes_names(dish_name=dish_name)
        return utils.toJSON(dishes)
    
    def get_user(self, email: str) -> str:
        user = self.dam.get_user(email=email)
        return utils.toJSON(user)
    
    def get_user_history(self, email: str) -> str:
        user = self.dam.get_user(email=email, add_history=True)
        return utils.toJSON(user)
    
    def get_full_meals_recommendation(self, email: str) -> str:
        rec_list = self.recommender.get_full_recommendation(email)
        return utils.toJSON(rec_list)
