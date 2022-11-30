from functools import wraps
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render

from controllers.main_controller import MainController
from .forms import DishToMealForm, LoginForm, MealForm2, UserForm, UserForm2
from .models import Dish, User


USER_MAIL = 'help@mail.ru'  # '6373b29a4b923a1729e4a30a' 

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


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.data['email']
            set_user(email)
            return HttpResponseRedirect('/user/')

    template_name = "user/login.html"
    form = LoginForm()
    data = {"form": form}
    return render(request, template_name, data)


def user_create(request):
    if request.method == 'POST':
        form = UserForm2(request.POST)
        if form.is_valid():
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
    else:
        form = UserForm2

    template_name = "user/update_profile.html"
    data = {"form": form}
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
        form = UserForm2(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/')
    else:
        form = UserForm2(instance=user)
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
        form = MealForm2(request.POST,)
        if form.is_valid():
            MainContr.add_meal_to_user(USER_MAIL, form.data['meal_type'], form.data['date'])
            return HttpResponseRedirect('/menu/')
    else:
        form = MealForm2
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
    if request.POST:
        selected_dishes = request.POST.getlist('selected_dish')
        MainContr.add_dish_to_meal(USER_MAIL, date, selected_dishes)
        return HttpResponseRedirect('/menu/')
    data = {}
    data['meal_date'] = date
    if 'name' in request.GET.keys():
        name = request.GET['name']
        search_dishes = json.loads(MainContr.get_dishes_names(name))
        data['search_dishes'] = search_dishes
        # rec_dishes = json.loads(MainContr.get_full_meals_recommendation(USER_MAIL))
        # data['selected_dishes'] = rec_dishes
        data['name'] = name
    else:
        data['search_dishes'] = []
        data['name'] = ''
    template_name = "menu/meal/add_dish.html"
    return render(request, template_name, data)



# @authorize
# def dish_to_meal(request, meal_id):
#     print(request.GET)
#     print(request.GET.keys())
#     form = DishToMealForm(request.GET)
#     data = {"form": form, }
#     if 'name' in request.GET.keys():
#         if form.is_valid():
#             name = get_name_filter(form.data['name'])
#             dishes = Dish.objects(name__icontains=name)
#         else: 
#             dishes = ['Нет блюд по данным фильтрам']
#         print(dishes)
#         data['search_dishes'] = dishes
#     # elif get_name_filter(None):
#     template_name = "menu/meal/select_dish.html"
#     return render(request, template_name, data)


@authorize
def dish_to_meal2(request, meal_id):
    print(request.GET)
    print(request.GET.keys())
    data = {}
    if 'name' in request.GET.keys():
        name = request.GET['name']
        dishes = Dish.objects(name__icontains=name)
        data['search_dishes'] = dishes
        data['name'] = name
        if 'dish' in request.GET.keys():
            print(request.GET['dish'])
            print(type(request.GET['dish']))
            selected_dishes = Dish.objects(id__in=[request.GET['dish']])
            data['selected_diishes'] = selected_dishes
    else:
        data['search_dishes'] = []
        data['name'] = ''
    # elif get_name_filter(None):
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
