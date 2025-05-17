from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home , name='Home'),  # Home page view
    path('proyectos/', views.Proyectos , name='Proyectos'),  # Projects page view
    path('perfil/', views.Perfil , name='Perfil'),  # Profile page view
    path('proyectos_detail/', views.ProyectosDetail , name='ProyectosDetail'), # Project details page view
    path('perfil/postulaciones/', views.MisPostulaciones, name='Postulaciones'),
    path('perfil/proyectos/', views.MisProyectos, name='MisProyectos'),
    path('perfil/editar/', views.EditarPerfil, name='EditarPerfil'),  # Edit profile page view
    path('login/', views.Login , name='Login'),  # Login page view
    path('logout/', views.Logout , name='Logout'),
    path('signup/', views.Signup , name='Signup'),  # Signup page view
    path('reset_password/', views.ResetPassword , name='ResetPassword'),  # Reset password page view
    path('subir_proyecto/', views.SubirProyecto , name='SubirProyecto'),  # Upload project page view
]
