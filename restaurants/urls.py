from django.urls import path

from . import views


app_name = 'home_page'
urlpatterns = [
    # ex: /restaurants/
    path('home_page', views.index, name='index'),
    path('restaurants/',views.global_restaurant, name='global_restaurant'),
    path('restaurants/<int:restaurant_id>/', views.detail_restaurant, name='detail_restaurant'),
    path('restaurants/<int:restaurant_id>/remove_burger/<int:burger_id>/', views.remove_burger, name='remove_burger'),
    path('restaurants/<int:restaurant_id>/remove_restaurant/', views.remove_restaurant, name='remove_restaurant'),
    path('restaurants/<int:restaurant_id>/update_burger/<int:burger_id>/', views.update_burger, name='update_burger'),
    path('restaurants/<int:restaurant_id>/update_restaurant/', views.update_restaurant, name='update_restaurant'),
    path('settings/', views.settings, name='settings'),
    path('settings/add_burger/', views.add_burger, name='add_burger'),
    path('settings/add_restaurant/', views.add_restaurant, name='add_restaurant'),

]