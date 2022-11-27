from functools import wraps

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import DishToMealForm, LoginForm, MealForm, UserForm
from .models import Dish, User


# None
USER_ID = '6373b29a4b923a1729e4a30a' 


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if USER_ID is None: 
            return HttpResponseRedirect('/login/')
        return f(*args, **kws)  
    return decorated_function


def set_user(id: str) -> None:
    global USER_ID
    USER_ID = id


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST['email'])
            set_user(user.id)
            return HttpResponseRedirect('/user/')

    template_name = "user/login.html"
    form = LoginForm()
    data = {"form": form}
    return render(request, template_name, data)


@authorize
def main(request):
    return render(request, "main.html")


@authorize
def user_profile(request):
    user = User.objects.get(id=USER_ID)
    data = {"user": user}
    return render(request, "user/profile.html", data)


@authorize
def user_update(request):
    user = User.objects.get(id=USER_ID)
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
    user = User.objects.get(id=USER_ID)
    return render(request, "menu/main.html", {"meals": user.meals})


def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm

    template_name = "user/update_profile.html"
    data = {"form": form}
    return render(request, template_name, data)


@authorize
def meal_delete(request, id):
    user = User.objects.get(id=USER_ID)
    del user.meals[id]
    user.save()
    return HttpResponseRedirect('/menu/')


@authorize
def meal_create(request):
    user = User.objects.get(id=USER_ID)
    if request.method == 'POST':
        form = MealForm(user, request.POST,)
        if form.is_valid() and request.POST['meal_type'] and request.POST['dishes'] and request.POST['date']:
            form.save()
            return HttpResponseRedirect('/menu/')
    else:
        form = MealForm(parent_document=User, )
    
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
def dish_to_meal(request, meal_id):
    print(request.GET)
    print(request.GET.keys())
    form = DishToMealForm(request.GET)
    data = {"form": form, }
    if 'name' in request.GET.keys():
        if form.is_valid():
            name = get_name_filter(form.data['name'])
            dishes = Dish.objects(name__icontains=name)
        else: 
            dishes = ['Нет блюд по данным фильтрам']
        print(dishes)
        data['search_dishes'] = dishes
    # elif get_name_filter(None):
    template_name = "menu/meal/select_dish.html"
    return render(request, template_name, data)


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
def dish_view(request, id):
    dish = Dish.objects(id=id)[0]
    template_name = "menu/dish.html"
    data = {"dish": dish}
    return render(request, template_name, data)
