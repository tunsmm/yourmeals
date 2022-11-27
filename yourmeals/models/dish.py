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
