from django import forms

from .models import STRATEGY_CHOICES, GENDER_CHOICES, MEAL_TYPE_CHOICES
  

class UserForm(forms.Form):
    email = forms.EmailField(help_text='yourmail@mail.ru', label=('Электронная почта'), )
    name = forms.CharField(help_text='Иван Иванов', label=('Имя'), )
    age = forms.IntegerField()
    weight = forms.FloatField()
    height = forms.FloatField()
    strategy = forms.ChoiceField(choices=STRATEGY_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)


class MealForm(forms.Form):
    meal_type = forms.ChoiceField(choices=MEAL_TYPE_CHOICES)
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class LoginForm(forms.Form):
    email = forms.EmailField(label='Ваша почта', required=True)
