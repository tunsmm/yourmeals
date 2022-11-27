import datetime

import mongoengine


mongoengine.connect(db="yourmeals", host="localhost", port=27017, alias="mydb-alias")

MEAL_TYPE_CHOICES = [
    ('Light', 'Перекус'),
    ('Full', 'Полноценный'),
]

GENDER_CHOICES = [
    ('Woman', 'Женщина'),
    ('Man', 'Мужчина'),
]

STRATEGY_CHOICES = [
    ('health', 'Поддержание веса'),
    ('loss', 'Похудение'),
    ('gain', 'Набор веса'),
]


class Dish(mongoengine.Document):
    name = mongoengine.StringField()
    calories = mongoengine.IntField()
    proteins = mongoengine.IntField()
    fats = mongoengine.IntField()
    carbohydates = mongoengine.IntField()
    recipe = mongoengine.StringField()
    description = mongoengine.StringField()
    preparing_time = mongoengine.StringField()
    ingredients = mongoengine.ListField()
    portions = mongoengine.IntField()
    tags = mongoengine.ListField(mongoengine.StringField())
    img_src = mongoengine.StringField()
    
    # Meta information
    meta = {
        "db_alias": "mydb-alias", 
        "collection": "dishes",
        "ordering": ["name"],
    }
    
    def __str__(self):
        return self.name


class Meal(mongoengine.EmbeddedDocument):
    global MEAL_TYPE_CHOICES
    meal_type = mongoengine.StringField(choices=MEAL_TYPE_CHOICES)
    dishes = mongoengine.ListField(mongoengine.ReferenceField(Dish))
    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    
    def __str__(self):
        return str(self.date) + self.meal_type


class User(mongoengine.Document):
    global GENDER_CHOICES
    global STRATEGY_CHOICES
    email = mongoengine.EmailField(required=True, unique=True)
    name = mongoengine.StringField(default="Пользователь")
    weight = mongoengine.FloatField(default=60, min_value=1, max_value=500)
    height = mongoengine.FloatField(default=160, min_value=1, max_value=300)
    calories = mongoengine.IntField(default=1000, min_value=0, max_value=20000)
    history = mongoengine.EmbeddedDocumentListField(Meal)
    full_meals = mongoengine.IntField(default=0, min_value=0, max_value=7)
    light_meals = mongoengine.IntField(default=0, min_value=0, max_value=7)
    gender = mongoengine.StringField(choices=GENDER_CHOICES)
    strategy = mongoengine.StringField(choices=STRATEGY_CHOICES)

    # Meta information
    meta = {
        "db_alias": "mydb-alias",
        "collection": "users",
        'ordering': ['-name'],
    }

    def __str__(self):
        return self.name