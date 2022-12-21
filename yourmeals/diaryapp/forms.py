from django import forms

from .models import STRATEGY_CHOICES, GENDER_CHOICES, MEAL_TYPE_CHOICES
  

class UserForm(forms.Form):
    email = forms.EmailField(help_text='yourmail@mail.ru', label=('Электронная почта'), )
    name = forms.CharField(help_text='Иван Иванов', label=('Имя'), )
    age = forms.IntegerField(label=('Возраст'),)
    weight = forms.FloatField(label=('Вес'),)
    height = forms.FloatField(label=('Рост'),)
    strategy = forms.ChoiceField(choices=STRATEGY_CHOICES, label=('Цель диеты'),)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label=('Пол'),)


class MealForm(forms.Form):
    meal_type = forms.ChoiceField(choices=MEAL_TYPE_CHOICES, label=('Тип приема пищи'),)
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label=('Дата приема пищи'),)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Ваша почта', required=True)
