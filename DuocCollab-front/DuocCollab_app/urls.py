from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home , name='Home'),  # Home page view
    path('login/', views.Login , name='Login'),  # Login page view
    path('logout/', views.Logout , name='Logout'),
    path('proyectos/', views.Proyectos , name='Proyectos'),  # Projects page view
    path('signup/', views.Signup , name='Signup'),  # Signup page view
    path('reset_password/', views.ResetPassword , name='ResetPassword'),  # Reset password page view
    path('perfil/', views.Perfil , name='Perfil'),  # Profile page view
    path('perfil/editar/', views.EditarPerfil, name='EditarPerfil'),  # Edit profile page view
    path('perfil/proyectos/', views.MisProyectos, name='MisProyectos'),
    path('subir_proyecto/', views.SubirProyecto , name='SubirProyecto'),  # Upload project page view
    path('proyectos_detail/', views.ProyectosDetail , name='ProyectosDetail'), # Project details page view
    path('perfil/postulaciones/', views.MisPostulaciones, name='Postulaciones'),
    path('escuelas/', views.Escuelas , name='Escuelas'),  # Schools page view

    
    path('admin/login/', views.AdminLogin , name='AdminLogin'),  # Admin login page view
    path('admin/', views.Admin , name='Admin'),  # Admin page view
    path('admin/inicio/', views.Inicio , name='Inicio'),  # Admin Home page view
    path('admin/escuela/', views.EscuelasAdmin , name='EscuelasAdmin'),  # Admin Schools page view
    path('admin/carrera/', views.Carreras , name='Carreras'),  # Admin Careers page view
    path('admin/sede/', views.Sede , name='Sede'),  # Admin Campus page view
    path('admin/sede_escuela/', views.SedeEscuela , name='SedeEscuela'),  # Admin School campus page view
    path('admin/usuario/', views.Usuarios , name='Usuarios'),  # Admin Users page view
    path('admin/etiqueta/', views.Etiquetas , name='Etiquetas'),  # Admin Tags page view
    path('admin/proyecto/', views.ProyectosAdmin , name='ProyectosAdmin'),  # Admin projects page view
    path('admin/proyecto_etiqueta/', views.ProyectoEtiqueta , name='ProyectoEtiqueta'),  # Admin Project tag page view
    path('admin/integrantes_proyecto/', views.IntegrantesProyecto , name='IntegrantesProyecto'),  # Admin Project members page view
    path('admin/postulacion/', views.Postulaciones , name='PostulacionesAdmin'),  # Admin Applications page view
    

]
