from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("menu/", views.user_menu, name="menu"),
    path("menu/meal/create/", views.meal_create, name="meal-new"),
    path("menu/meal/<str:date>/<str:time>/delete/", views.meal_delete, name="meal-delete"),
    path("menu/dish/<str:name>/", views.dish_view, name="dish-view"),
    path("menu/meal/<str:date>/<str:time>/dish_delete/<str:name>/", views.dish_delete_on_meal, name="dish-delete"),
    
    path("menu/meal/add/<str:date>/<str:time>/", views.dish_to_meal, name="dish-to-meal"),
    path("menu/search/", views.get_dishes_by_name, name="dishes-by-name"),
    
    path("user/", views.user_profile, name="user"),
    path("user/update/", views.user_update, name="user-update"),
    
    path("signup/", views.user_create, name="signup"),
    
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
