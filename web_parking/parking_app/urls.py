from django.urls import path
from . import views

app_name = 'parking_app'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('park/', views.park_vehicle, name='park'),
    path('remove/', views.remove_vehicle, name='remove'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
