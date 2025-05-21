from django.shortcuts import render, redirect
from .api_client import iniciar_sesion, consulta_sede, consulta_carrera, consulta_escuela, registrar_usuario, trae_img_perfil, consulta_sede_escuela, consulta_etiqueta, consulta_usuario, consulta_proyecto
from .api_client import consuta_proyecto_etiqueta, consulta_integrantes, consulta_postulacion
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
  usuario = request.session.get('usuario')

    # Opcional: Traer imagen desde API
  url_perfil, url_portada = trae_img_perfil(usuario['FOTO_PERFIL'], usuario['FOTO_PORTADA'])

  contexto = {
    'usuario': usuario,
    'foto_perfil': url_perfil,
    'foto_portada': url_portada
  }

  return render(request, 'editar_perfil.html', contexto)


def Admin(request):
  return render(request, 'admin/admin.html')

def Carreras(request):
  if request.method == 'GET':
    contexto = {
      'carreras':consulta_carrera(),
      'escuelas':consulta_escuela()
    }
  return render(request, 'admin/carrera.html', contexto)


def Escuelas(request):
  if request.method == 'GET':
    contexto = {
      'escuelas':consulta_escuela()
    }
  return render(request, 'admin/escuela.html', contexto)

def Etiquetas(request):
  if request.method == 'GET':
    contexto = {
      'etiquetas':consulta_etiqueta()
    }
  return render(request, 'admin/etiqueta.html', contexto)

def IntegrantesProyecto(request):
  if request.method == 'GET':
    contexto = {
      'integrantes':consulta_integrantes(),
      'proyectos':consulta_proyecto(),
      'usuarios':consulta_usuario()
    }
  return render(request, 'admin/integrantes_proyecto.html', contexto)

def Postulaciones(request):
  if request.method == 'GET':
    contexto = {
      'postulaciones':consulta_postulacion(),
      'proyectos':consulta_proyecto(),
      'usuarios':consulta_usuario()
    }
  return render(request, 'admin/postulacion.html', contexto)

def ProyectoEtiqueta(request):
  if request.method == 'GET':
    contexto = {
      'proyecto_etiqueta':consuta_proyecto_etiqueta(),
      'etiquetas':consulta_etiqueta(),
      'proyectos':consulta_proyecto()
    }
  return render(request, 'admin/proyecto_etiqueta.html', contexto)

def ProyectosAdmin(request):
  if request.method == 'GET':
    contexto = {
      'proyectos':consulta_proyecto(),
      'carreras':consulta_carrera(),
      'sedes':consulta_sede(),
      'usuarios':consulta_usuario(),
    }
  return render(request, 'admin/proyecto.html', contexto)

def SedeEscuela(request):
  if request.method == 'GET':
    contexto = {
      'sedes':consulta_sede(),
      'sede_escuela':consulta_sede_escuela(),
      'escuelas':consulta_escuela()
    }
  return render(request, 'admin/sede_escuela.html', contexto)

def Sede(request):
  if request.method == 'GET':
    contexto = {
      'sedes':consulta_sede()
    }
  return render(request, 'admin/sede.html', contexto)

def Usuarios(request):
  if request.method == 'GET':
    contexto = {
      'usuarios':consulta_usuario(),
      'carreras':consulta_carrera(),
      'etiquetas':consulta_etiqueta(),
    }
  return render(request, 'admin/usuario.html', contexto)

def Inicio(request):
  return render(request, 'admin/home.html')
