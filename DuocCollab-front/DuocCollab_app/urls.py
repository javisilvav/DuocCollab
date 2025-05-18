from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('proyectos/', views.Proyectos, name='Proyectos'),
    path('perfil/', views.Perfil, name='Perfil'),
    path('proyectos_detail/', views.ProyectosDetail, name='ProyectosDetail'),
    path('perfil/postulaciones/', views.MisPostulaciones, name='Postulaciones'),
    path('perfil/proyectos/', views.MisProyectos, name='MisProyectos'),
    path('perfil/editar/', views.EditarPerfil, name='EditarPerfil'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('signup/', views.Signup, name='Signup'),
    path('reset_password/', views.ResetPassword, name='ResetPassword'),
    path('subir_proyecto/', views.SubirProyecto, name='SubirProyecto'),
]