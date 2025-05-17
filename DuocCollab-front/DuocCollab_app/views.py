from django.shortcuts import render, redirect
from .api_client import iniciar_sesion, consulta_sede, consulta_carrera, consulta_escuela, registrar_usuario, trae_img_perfil
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .decorators import login_required

def Home(request):
  return render(request, 'index.html')  

def Proyectos(request):
  return render(request, 'proyectos.html')


@login_required
def Perfil(request):
  usuario = request.session.get('usuario')

  url_perfil, url_portada = trae_img_perfil(usuario['FOTO_PERFIL'], usuario['FOTO_PORTADA'])

  print(url_perfil)
  print(url_portada)
  contexto = {
    'usuario':usuario,
    'foto_perfil': url_perfil,
    'foto_portada': url_portada
  }
  
  return render(request, 'perfil.html', contexto)

def ProyectosDetail(request):
  return render(request, 'proyectos_detail.html')

def MisPostulaciones(request):
  return render(request, 'mispostulaciones.html')

def MisProyectos(request):
  return render(request, 'misproyectos.html')

def Login(request):
  if request.method == 'GET':
    return render(request, 'login.html')
  if request.method == 'POST':
    correo = request.POST.get('correo')
    contra = request.POST.get('contrasena')
    
    respuesta = iniciar_sesion(correo, contra)
    if 'error' not in respuesta:
      request.session['usuario'] = respuesta
      return redirect('Home')
    else:
      return render(request, 'login.html',{'error':respuesta['error']})

def Logout(request):
    request.session.flush() 
    return redirect('Login')


def obtener_ruta_sin_perfil():
    ruta = os.path.join(settings.BASE_DIR, 'DuocCollab_app', 'static', 'img', 'sin_perfil.png')
    return ruta

def Signup(request):
  if request.method == 'GET':
    contexto = {
      'sedes':consulta_sede(),
      'carreras':consulta_carrera(),
      'escuelas':consulta_escuela()
    }
    return render(request, 'signup.html', contexto)
  if request.method == 'POST':
    data = {
      'NOMBRE': request.POST.get('nombre'),
      'APELLIDO': request.POST.get('apellido'),
      'CORREO': request.POST.get('correo'),
      'CONTRASENIA': request.POST.get('contrasena'),
      'ID_CARRERA': request.POST.get('carrera'),
      'INTERESES': 'Sin intereses',
      'FOTO_PERFIL': '',
      'FOTO_PORTADA': ''
    }
    archivos = {}
    if 'foto_perfil' not in request.FILES:
      with open(obtener_ruta_sin_perfil(), 'rb') as f:
            archivos['FOTO_PERFIL'] = SimpleUploadedFile('sin_perfil.png', f.read(), content_type='image/png')
            
    if 'foto_portada' not in request.FILES:
      with open(obtener_ruta_sin_perfil(), 'rb') as f:
            archivos['FOTO_PORTADA'] = SimpleUploadedFile('sin_perfil.png', f.read(), content_type='image/png')

    response = registrar_usuario(data,archivos)

    if response.ok:
      return redirect('Login')
    else:
      try:
        error = response.json().get('error','Error al registrar usuario.')
      except Exception:
        error = response.text
        print(error)
      return redirect('Signup')


def ResetPassword(request):
  return render(request, 'reset_password.html')

def SubirProyecto(request):
  return render(request, 'subir_proyecto.html')

def EditarPerfil(request):
  return render(request, 'editar_perfil.html')