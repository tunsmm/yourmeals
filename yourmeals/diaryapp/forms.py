import datetime

from django import forms
from mongodbforms import DocumentForm, EmbeddedDocumentForm

from .models import Meal, User, STRATEGY_CHOICES, GENDER_CHOICES, MEAL_TYPE_CHOICES


class UserForm(DocumentForm):
    class Meta:
        document = User
        fields = ("email", "name", "full_meals", "light_meals", "weight", "height", "calories", )
        

class UserForm2(forms.Form):
    email = forms.EmailField(help_text='yourmail@mail.ru', label=('Электронная почта'), )
    name = forms.CharField(help_text='Иван Иванов', label=('Имя'), )
    age = forms.IntegerField()
    weight = forms.FloatField()
    height = forms.FloatField()
    strategy = forms.ChoiceField(choices=STRATEGY_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)


class MealForm2(forms.Form):
    meal_type = forms.ChoiceField(choices=MEAL_TYPE_CHOICES)
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


# class MealForm(EmbeddedDocumentForm):
#     class Meta:
#         document = Meal
#         embedded_field_name = 'meals'
#         fields = ("meal_type", "dishes", "date", )
#         widgets = {
#             'date': forms.DateInput(),
#         }


class DishToMealForm(forms.Form):
    name = forms.CharField(help_text='Название блюда', label=('Название блюда'), )
    # calories
    # proteins
    # fats
    # carbohydates
    # recipe
    # preparing_time
    # ingredients
    # portions
    # tags


class LoginForm(forms.Form):
    email = forms.EmailField(label='Ваша почта', required=True)
