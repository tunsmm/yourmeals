from yourmeals.src.data_access.data_access_module import DataAccessModule as DAM
from yourmeals.src.models.meal import get_meal
import yourmeals.src.models as models
import utils


class MainController:
    def __init__(self) -> None:
        self.dam = DAM()
        
    def create_user(self, email: str, name: str, weight: float, height: float, strategy: str, gender: str,):
        user = models.user.User(
            email=email,
            name=name,
            weight=weight,
            height=height,
            gender=gender,
            strategy=strategy,
        )
        self.dam.save_user(user)
        
    def update_user(self, email: str, name: str, weight: float, height: float, strategy: str, gender: str):
        user = self.dam.get_user(email=email)
        user.name = name
        user.weight = weight
        user.height = height
        user.strategy = strategy
        user.gender = gender
        self.dam.save_user(user)
    
    def add_meal_to_user(self, email: str, meal_type: str, dishes: list[str], date):
        user = self.dam.get_user(email=email)
        meal = get_meal(meal_type)
        meal.set_date(date)
        for str_dish in dishes:
            meal.add_dish(str_dish)
        user.add_meal(meal)
        self.dam.save_user(user)
        
    def delete_meal(self, email: str, date):
        user = self.dam.get_user(email=email)
        user.delete_meal(date)
        self.dam.save_user(user)
        
    def add_dish_to_meal(self, email: str, date, dishes: list[str]):
        user = self.dam.get_user(email=email)
        meal = user.get_meal(date)
        for str_dish in dishes:
            meal.add_dish(str_dish)
                    
    def delete_dish_on_meal(self, email: str, date, dish_name: str):
        user = self.dam.get_user(email=email)
        meal = user.get_meal(date)
        dish = meal.get_dish(dish_name)
        del dish
    
    def get_dish(self, dish_name: str) -> str:
        dish = self.dam.get_dish(dish_name=dish_name)
        return utils.toJSON(dish)
    
    def get_user(self, email: str) -> str:
        user = self.dam.get_user(email=email)
        return utils.toJSON(user)
