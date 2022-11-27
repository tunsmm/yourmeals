from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("menu/", views.user_menu, name="menu"),
    path("menu/meal/create/", views.meal_create, name="meal-new"),
    path("menu/meal/<int:id>/delete/", views.meal_delete, name="meal-delete"),
    path("menu/dish/<str:id>/", views.dish_view, name="dish-view"),
    
    path("menu/meal/add/<int:meal_id>/", views.dish_to_meal, name="dish-to-meal"),
    path("menu/meal/add2/<int:meal_id>/", views.dish_to_meal2, name="dish-to-meal2"),
    
    path("user/", views.user_profile, name="user"),
    path("user/update/", views.user_update, name="user-update"),
    
    path("signup/", views.user_create, name="signup"),
    
    path("login/", views.login, name="login"),
]
