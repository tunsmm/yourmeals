from functools import wraps
import base64
import hashlib
import hmac
import json
import os

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv
from mongoengine.errors import NotUniqueError

from yourmeals.controllers.main_controller import MainController
from .forms import LoginForm, MealForm, UserForm


load_dotenv()

SECRET_USERMAIL_SALT = os.getenv("SECRET_USERMAIL_SALT")

MainContr = MainController()


def sign_data(data: str):
    """
    Return signed data
    """
    return hmac.new(
        SECRET_USERMAIL_SALT.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_email_from_signed_data(signed_data: str):
    email, sign = signed_data.split(".")
    email = base64.b64decode(email.encode()).decode()
    valid_sign = sign_data(email)
    if hmac.compare_digest(valid_sign, sign):
        return email


def read_usermail_cookies(request):
    email_cookie = request.COOKIES.get('email', None)
    if not email_cookie:
        return None
    valid_email = get_email_from_signed_data(email_cookie)
    return valid_email


def authorize(f):
    @wraps(f)
    def decorated_function(request, *args, **kws):
        USER_MAIL = read_usermail_cookies(request)
        if USER_MAIL is None or not MainContr.get_user(USER_MAIL): 
            return HttpResponseRedirect('/login/')
        return f(request, *args, **kws)  
    return decorated_function


def logout(request) -> None:
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('email')
    return response


def login(request):
    data = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.data['email']
            user = json.loads(MainContr.get_user(email=email))
            if user:
                response = HttpResponseRedirect('/user/')
                email_signed = base64.b64encode(
                    email.encode()
                ).decode() + '.' + sign_data(email)
                response.set_cookie(
                    key='email',
                    value=email_signed,
                    max_age=2000,
                )
                return response
            data["error"] = "Пользователя с данным логином не существует"
            
    template_name = "user/login.html"
    form = LoginForm()
    data["form"] = form
    return render(request, template_name, data)


def user_create(request):
    data = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                MainContr.create_user(
                    email=form.data['email'],
                    name=form.data['name'],
                    age=int(form.data['age']),
                    weight=float(form.data['weight']),
                    height=float(form.data['height']),
                    gender=form.data['gender'],
                    strategy=form.data['strategy'],
                )
                return HttpResponseRedirect('/')
            except NotUniqueError:
                data["error"] = "Пользователь с указанной почтой уже существует."
    else:
        form = UserForm
    template_name = "user/new.html"
    data["form"] = form
    return render(request, template_name, data)


@authorize
def main(request):
    return render(request, "main.html")


@authorize
def user_profile(request):
    user = read_usermail_cookies(request)
    user = json.loads(MainContr.get_user(email=user))
    data = {"user": user}
    return render(request, "user/profile.html", data)


@authorize
def user_update(request):
    user = read_usermail_cookies(request)
    user = json.loads(MainContr.get_user(email=user))
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/')
    else:
        form = UserForm(instance=user)
    template_name = "user/update_profile.html"
    data = {"form": form}
    return render(request, template_name, data)


@authorize
def user_menu(request):
    user = read_usermail_cookies(request)
    user = json.loads(MainContr.get_user(email=user))
    return render(request, "menu/main.html", {"meals": user['history']})


@authorize
def meal_delete(request, user, date):
    user = read_usermail_cookies(request)
    MainContr.delete_meal(email=user, date=date)
    return HttpResponseRedirect('/menu/')


@authorize
def meal_create(request):
    user = read_usermail_cookies(request)
    if request.method == 'POST':
        form = MealForm(request.POST,)
        if form.is_valid():
            MainContr.add_meal_to_user(user, form.data['meal_type'], form.data['date'])
            return HttpResponseRedirect('/menu/')
    else:
        form = MealForm
    template_name = "menu/meal/new.html"
    data = {"form": form}
    return render(request, template_name, data)


@authorize
def get_dishes_by_name(request):
    if request.GET['name']:
        name = request.GET['name']
        data = MainContr.get_dishes_names(name)
        return JsonResponse(json.loads(data), safe=False)
    return JsonResponse({"answer": None})


@authorize
def dish_to_meal(request, date=None):
    user = read_usermail_cookies(request)
    data = {}
    if request.POST:
        selected_dishes = request.POST.getlist('selected_dish')
        try:
            MainContr.add_dish_to_meal(user, date, selected_dishes)
        except ValueError as e:
            data['error'] = e
        if 'error' not in data.keys():
            return HttpResponseRedirect('/menu/')
    
    data['meal_date'] = date
    rec_dishes = json.loads(MainContr.get_full_meals_recommendation(user))
    data['rec_dishes'] = rec_dishes
    template_name = "menu/meal/add_dish.html"
    return render(request, template_name, data)


@authorize
def dish_view(request, name):
    dish = json.loads(MainContr.get_dish(name))
    template_name = "menu/dish.html"
    data = {"dish": dish}
    return render(request, template_name, data)


@authorize
def dish_delete_on_meal(request, date=None, name=None):
    user = read_usermail_cookies(request)
    MainContr.delete_dish_on_meal(user, date, name)
    return HttpResponseRedirect('/menu/')
