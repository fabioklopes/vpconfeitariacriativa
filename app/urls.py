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
]
