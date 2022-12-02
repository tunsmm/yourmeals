from functools import wraps
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from mongoengine.errors import DoesNotExist, NotUniqueError

from controllers.main_controller import MainController
from .forms import LoginForm, MealForm, UserForm


USER_MAIL = None

MainContr = MainController()


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if USER_MAIL is None: 
            return HttpResponseRedirect('/login/')
        return f(*args, **kws)  
    return decorated_function


def set_user(id: str) -> None:
    global USER_MAIL
    USER_MAIL = id
    

def logout(request) -> None:
    global USER_MAIL
    USER_MAIL = None
    return HttpResponseRedirect('/login/')


def login(request):
    data = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.data['email']
            try:
                MainContr.get_user(email=email)
                set_user(email)
                return HttpResponseRedirect('/user/')
            except DoesNotExist:
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
    template_name = "user/update_profile.html"
    data["form"] = form
    return render(request, template_name, data)


@authorize
def main(request):
    return render(request, "main.html")


@authorize
def user_profile(request):
    user = json.loads(MainContr.get_user(email=USER_MAIL))
    data = {"user": user}
    return render(request, "user/profile.html", data)


@authorize
def user_update(request):
    user = json.loads(MainContr.get_user(email=USER_MAIL))
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
    user = json.loads(MainContr.get_user(email=USER_MAIL))
    # print(user)
    return render(request, "menu/main.html", {"meals": user['history']})


@authorize
def meal_delete(request, date):
    MainContr.delete_meal(email=USER_MAIL, date=date)
    return HttpResponseRedirect('/menu/')


@authorize
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST,)
        if form.is_valid():
            MainContr.add_meal_to_user(USER_MAIL, form.data['meal_type'], form.data['date'])
            return HttpResponseRedirect('/menu/')
    else:
        form = MealForm
    template_name = "menu/meal/new.html"
    data = {"form": form}
    return render(request, template_name, data)


NAME_FILTER = ''


def get_name_filter(set_name=None):
    global NAME_FILTER
    if set_name and NAME_FILTER != set_name:
        NAME_FILTER = set_name
    return NAME_FILTER


@authorize
def dish_to_meal(request, date):
    data = {}
    if request.POST:
        selected_dishes = request.POST.getlist('selected_dish')
        try:
            MainContr.add_dish_to_meal(USER_MAIL, date, selected_dishes)
        except ValueError as e:
            data['error'] = e
        if 'error' not in data.keys():
            return HttpResponseRedirect('/menu/')
    
    data['meal_date'] = date
    rec_dishes = json.loads(MainContr.get_full_meals_recommendation(USER_MAIL))
    data['rec_dishes'] = rec_dishes
    if 'name' in request.GET.keys():
        name = request.GET['name']
        search_dishes = json.loads(MainContr.get_dishes_names(name))
        data['search_dishes'] = search_dishes
        data['name'] = name
    else:
        data['search_dishes'] = []
        data['name'] = ''
    template_name = "menu/meal/add_dish.html"
    return render(request, template_name, data)


@authorize
def dish_view(request, name):
    dish = json.loads(MainContr.get_dish(name))
    template_name = "menu/dish.html"
    data = {"dish": dish}
    return render(request, template_name, data)


@authorize
def dish_delete_on_meal(request, date, name):
    MainContr.delete_dish_on_meal(USER_MAIL, date, name)
    return HttpResponseRedirect('/menu/')
