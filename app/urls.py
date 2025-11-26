from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pricings/', views.pricing_list, name='pricing_list'),
    path('pricings/new/', views.pricing_create, name='pricing_create'),
    path('pricings/<int:pk>/', views.pricing_detail, name='pricing_detail'),
    path('pricings/<int:pk>/edit/', views.pricing_edit, name='pricing_edit'),
    path('costs/', views.costs_view, name='costs'),
    path('histories/', views.histories_view, name='histories'),

    path('finished-recipes/', views.finished_recipe_list, name='finished_recipe_list'),
    path('finished-recipes/new/', views.finished_recipe_create, name='finished_recipe_create'),
    path('finished-recipes/<int:pk>/', views.finished_recipe_detail, name='finished_recipe_detail'),
    path('finished-recipes/<int:pk>/edit/', views.finished_recipe_edit, name='finished_recipe_edit'),
    path('finished-recipes/<int:pk>/delete/', views.finished_recipe_delete, name='finished_recipe_delete'),

    path('api/inputs/', views.input_api_create, name='input_api_create'),
]
