from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home , name='Home'),  # Home page view
    path('proyectos/', views.Proyectos , name='Proyectos'),  # Projects page view
    path('ejemplo/', views.Ejemplo , name='Ejemplo'),
    path('perfil/', views.Perfil , name='Perfil'),  # Profile page view
    path('proyectos_detail/', views.ProyectosDetail , name='ProyectosDetail'), # Project details page view
]
