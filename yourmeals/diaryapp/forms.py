from django import forms
from mongodbforms import DocumentForm, EmbeddedDocumentForm

from .models import Meal, User


class UserForm(DocumentForm):
    class Meta:
        document = User
        fields = ("email", "name", "full_meals", "light_meals", "weight", "height", "calories", )


class MealForm(EmbeddedDocumentForm):
    class Meta:
        document = Meal
        embedded_field_name = 'meals'
        fields = ("meal_type", "dishes", "date", )
        widgets = {
            'date': forms.DateInput(),
        }


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
