from django import forms

from ..data_access.choices import STRATEGY_CHOICES, GENDER_CHOICES, MEAL_TYPE_CHOICES
  

class UserForm(forms.Form):
    email = forms.EmailField(help_text='yourmail@mail.ru', label=('Электронная почта'), )
    name = forms.CharField(help_text='Иван Иванов', label=('Имя'), min_length=2, max_length=100 )
    age = forms.IntegerField(label=('Возраст'), min_value=1, max_value=200)
    weight = forms.FloatField(label=('Вес'), min_value=1, max_value=500)
    height = forms.FloatField(label=('Рост'), min_value=1, max_value=300)
    strategy = forms.ChoiceField(choices=STRATEGY_CHOICES, label=('Цель диеты'),)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label=('Пол'),)


class MealForm(forms.Form):
    meal_type = forms.ChoiceField(choices=MEAL_TYPE_CHOICES, label=('Тип приема пищи'),)
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label=('Дата приема пищи'),)


class LoginForm(forms.Form):
    email = forms.EmailField(help_text='yourmail@mail.ru', label='Ваша почта', required=True)
