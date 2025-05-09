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