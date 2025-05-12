from django.shortcuts import render

def Home(request):
  return render(request, 'index.html')  

def Proyectos(request):
  return render(request, 'proyectos.html')

def Ejemplo(request):
  return render(request, 'ejemplo.html')

def Perfil(request):
  return render(request, 'perfil.html')

def ProyectosDetail(request):
  return render(request, 'proyectos_detail.html')

def MisPostulaciones(request):
  return render(request, 'mispostulaciones.html')

def MisProyectos(request):
  return render(request, 'misproyectos.html')

def Login(request):
  return render(request, 'login.html')

def Signup(request):
  return render(request, 'signup.html')

def ResetPassword(request):
  return render(request, 'reset_password.html')