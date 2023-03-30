from datetime import datetime, time, date

import pytest

from .dish import Dish
from .meal import Meal, get_meal
from .user import User


@pytest.fixture()
def dish():
    return Dish(
        name='DishName',
        calories=500.1,
        proteins=30.7,
        fats=50.2,
        carbohydrates=123.2,
        recipe='Smash them all',
        preparing_time='30 min',
        description='Empty desc',
        ingredients={
            'Milk': 100,
            'Bread': 200,
        },
        portions=5,
        tags=['Main', 'Breakfast'],
        img_src='http'
    )
    
@pytest.fixture()
def dish2():
    return Dish(
        name='DishName2',
        calories=500.1,
        proteins=30.7,
        fats=50.2,
        carbohydrates=123.2,
        recipe='Smash them all',
        preparing_time='30 min',
        description='Empty desc',
        ingredients={
            'Milk': 100,
            'Bread': 200,
        },
        portions=5,
        tags=['Main', 'Breakfast'],
        img_src='http'
    )
    

@pytest.fixture()
def dish3():
    return Dish(
        name='DishName2',
        calories=3500.1,
        proteins=40.7,
        fats=60.2,
        carbohydrates=133.2,
        recipe='Smash them all',
        preparing_time='30 min',
        description='Empty desc',
        ingredients={
            'Milk': 100,
            'Bread': 200,
        },
        portions=1,
        tags=['Main', 'Breakfast'],
        img_src='http'
    )


class TestDish:
    def test_calories_on_portion_ok(self, dish) -> None:
        assert dish.calories_on_portion == (dish.calories // dish.portions)
        
    def test_calories_on_portion_fail(self, dish2) -> None:
        assert dish2.calories_on_portion != 0
        
    def test_compare_dishes(self, dish, dish2) -> None:
        assert dish != dish2


@pytest.fixture()
def meal():
    return Meal()


@pytest.fixture()
def meal2(dish2):
    return Meal(
        dishes=[dish2]
    )


class TestMeal:
    def test_calculate_sum_calories(self, meal, dish) -> None:
        meal.add_dish(dish)
        assert meal.sum_calories == dish.calories_on_portion
        
    def test_get_dish(self, meal2, dish2) -> None:
        assert isinstance(meal2.get_dish(dish2.name), Dish)
        assert meal2.get_dish("Тест") is None
        
    def test_delete_dish(self, meal2, dish2) -> None:
        meal2.delete_dish(dish2.name)
        assert meal2.get_dish(dish2.name) is None

    def test_add_dish(self, meal2, dish, dish3) -> None:
        with pytest.raises(ValueError):
            meal2.add_dish(dish3)
        assert len(meal2.dishes) == 1
        meal2.add_dish(dish)
        assert len(meal2.dishes) == 2    



@pytest.fixture
def user():
    meal = Meal(
        dishes=[
            Dish(
                name="Oatmeal",
                calories=750,
                proteins=25,
                fats=15,
                carbohydrates=127,
                recipe="1. Cook oats and water over medium heat. 2. Stir in toppings.",
                description="A warm and filling breakfast dish.",
                preparing_time="10 minutes",
                ingredients=[{"Rolled Oats": "1/2 of cup"}],
                portions=5,
                tags=["Breakfast", "Healthy", "Vegetarian"],
                img_src="oatmeal.jpg",
            )
        ],
        date=date(2023, 3, 11),
        time=time(8, 0),
    )
    meal.meal_type = 'light'
    u = User(
        email="john@example.com",
        name="John",
        age=30,
        weight=70.0,
        height=1.8,
        strategy="health",
        gender="man",
    )
    u.add_meal(meal)
    yield u


class TestUser:

    def test_user_creation(self, user):
        assert user.email == "john@example.com"
        assert user.name == "John"
        assert user.age == 30
        assert user.weight == 70.0
        assert user.height == 1.8
        assert user.strategy == "health"
        assert user.gender == "man"
        assert len(user.history) == 1

    def test_add_meal(self, user):
        new_meal = Meal(
            dishes=[
                Dish(
                    name="Chicken Breast",
                    calories=600,
                    proteins=45,
                    fats=13,
                    carbohydrates=230,
                    recipe="1. Preheat the oven. 2. Season chicken with salt and pepper. 3. Bake for 25 minutes.",
                    description="A simple and protein-packed meal.",
                    preparing_time="30 minutes",
                    ingredients=[{"Chicken Breast": "6 oz"}],
                    portions=4,
                    tags=["Dinner", "Protein", "Healthy"],
                    img_src="chicken.jpg",
                )
            ],
            date=date(2023, 3, 11),
            time=time(18, 0),
        )
        new_meal.meal_type = 'full'
        user.add_meal(new_meal)
        assert len(user.history[str(new_meal.date)]) == 2

    def test_get_meal(self, user):
        meal = user.get_meal(date(2023, 3, 11), time(8, 0))
        assert isinstance(meal, Meal)
        assert meal.dishes[0].name == "Oatmeal"
        
    @pytest.fixture
    def user2(self):
        dishes = [Dish(name='dish1', calories=100, proteins=10, fats=5, carbohydrates=20, recipe='recipe1', 
                       description='description1', preparing_time='10 minutes', ingredients=[], portions=2, tags=[], 
                       img_src='image1.jpg')]
        meal = Meal(dishes=dishes, date=date(2020, 7, 10), time=time(10, 0))
        meal.meal_type = 'full'
        u = User(email='test@example.com', name='John Doe', age=30, weight=70.5, height=175.0, 
                    strategy='loss', gender='man', )
        u.add_meal(meal)
        yield u

    @pytest.fixture
    def new_meal(self):
        dishes = [Dish(name='dish2', calories=150, proteins=15, fats=8, carbohydrates=25, recipe='recipe2', 
                       description='description2', preparing_time='15 minutes', ingredients=[], portions=3, tags=[], 
                       img_src='image2.jpg')]
        meal = Meal(dishes=dishes, date=datetime.now().date(), time=datetime.now().time())
        meal.meal_type = 'full'
        yield meal

    def test_set_meal2(self, user2, new_meal):
        assert len(user2.history) == 1

        user2.set_meal(date=date(2020, 7, 10), time=time(10, 0), new_meal=new_meal)

        assert user2.history[str(date(2020, 7, 10))] == new_meal

    def teardown_method(self, user):
        del user
