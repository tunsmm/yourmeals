from yourmeals.src.data_access.data_access_module import DataAccessModule as DAM
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
    
    def add_meal_to_user(self):
        pass
    
    def add_dish_to_meal(self):
        pass
    
    def get_dish(self, dish_name: str) -> str:
        dish = self.dam.get_dish(dish_name=dish_name)
        return utils.toJSON(dish)
    
    def get_user(self, email: str) -> str:
        user = self.dam.get_user(email=email)
        return utils.toJSON(user)
