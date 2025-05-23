from django.shortcuts import render, redirect
from .api_client import (
    iniciar_sesion,
    consulta_sede,
    consulta_carrera,
    consulta_escuela, 
    registrar_usuario, 
    trae_img_perfil, 
    consulta_mis_proyectos,
    consulta_mis_postulaciones,
    consulta_proyectos,
    actualizar_usuario
)
import requests
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .decorators import login_required

def Home(request):
    return render(request, 'index.html')  

def Proyectos(request):
    data = consulta_proyectos(request)
    for proyecto in data:
        filename = proyecto.get('FOTO_PROYECTO')

        if filename:
            proyecto['FOTO_PROYECTO'] = f"http://127.0.0.1:5050/api/uploads/imagen_proyecto/{filename}"
        else:
            proyecto['FOTO_PROYECTO'] = '/static/img/sin_perfil.png'  # fallback local
    contexto = {
        'proyectos': data,
    }
    return render(request, 'proyectos.html', contexto)

@login_required
def Perfil(request):
    usuario = request.session.get('usuario')
    url_perfil, url_portada = trae_img_perfil(usuario['FOTO_PERFIL'], usuario['FOTO_PORTADA'])
    contexto = {
        'usuario': usuario,
        'foto_perfil': url_perfil,
        'foto_portada': url_portada
    }
    return render(request, 'perfil.html', contexto)

def ProyectosDetail(request):
    return render(request, 'proyectos_detail.html')




@login_required
def ImagenProtegida(request, filename):
    token = request.session.get('jwt_token')
    if not token:
        print('No autorizado: No hay token')
        return

    url = f'http://localhost:5000/api/uploads/imagen_proyecto/{filename}'
    print(f"URL solicitada: {url}")
    print(f"Usando token: {token}")

    try:
        response = requests.get(url, headers={
            'Authorization': f'Bearer {token}'
        }, stream=True)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            print(f"[OK] Imagen obtenida. Content-Type: {content_type}, tamaño: {len(response.content)} bytes")
        else:
            print(f"[ERROR] No se pudo obtener la imagen. Código HTTP: {response.status_code}")
            print(f"Respuesta: {response.text}")

    except Exception as e:
        print(f"[EXCEPCIÓN] Error al obtener la imagen: {e}")


def MisProyectos(request):
    data = consulta_mis_proyectos(request)
    for proyecto in data:
        filename = proyecto.get('FOTO_PROYECTO')

        if filename:
            proyecto['FOTO_PROYECTO'] = f"http://127.0.0.1:5050/api/uploads/imagen_proyecto/{filename}"
        else:
            proyecto['FOTO_PROYECTO'] = '/static/img/sin_perfil.png'  # fallback local
    contexto = {
        'proyectos': data,
    }
    return render(request, 'misproyectos.html', contexto)

def MisPostulaciones(request):
    data = consulta_mis_postulaciones(request)
    
    for postulacion in data:
        proyecto = postulacion.get('PROYECTO', {})
        filename = proyecto.get('FOTO_PROYECTO')
        
        if filename:
            proyecto['FOTO_PROYECTO'] = f"http://127.0.0.1:5050/api/uploads/imagen_proyecto/{filename}"
        else:
            proyecto['FOTO_PROYECTO'] = '/static/img/sin_perfil.png'  # fallback local
    contexto = {
        'postulaciones': data
    }
    return render(request, 'mispostulaciones.html', contexto)


def Login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contra = request.POST.get('contrasena')
        
        respuesta = iniciar_sesion(correo, contra)
        if 'error' not in respuesta:
            usuario = respuesta['usuario']
            token = respuesta['token']

            request.session['jwt_token'] = token
            request.session['usuario'] = usuario

            return redirect('Home')
        else:
            return render(request, 'login.html', {'error': respuesta['error']})

def Logout(request):
    request.session.flush()
    return redirect('Login')

def obtener_ruta_sin_perfil():
    ruta = os.path.join(settings.BASE_DIR, 'DuocCollab_app', 'static', 'img', 'sin_perfil.png')
    return ruta

def Signup(request):
    if request.method == 'GET':
        contexto = {
            'sedes': consulta_sede(request),
            'carreras': consulta_carrera(request),
            'escuelas': consulta_escuela(request)
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

        response = registrar_usuario(data, archivos)

        if response.ok:
            return redirect('Login')
        else:
            try:
                error = response.json().get('error', 'Error al registrar usuario.')
            except Exception:
                error = response.text
                print(error)
            return redirect('Signup')

def ResetPassword(request):
    return render(request, 'reset_password.html')

@login_required
def SubirProyecto(request):
    return render(request, 'subir_proyecto.html')


@login_required
def EditarPerfil(request):
    if request.method == 'GET':
        usuario = request.session.get('usuario')
        url_perfil, url_portada = trae_img_perfil(usuario['FOTO_PERFIL'], usuario['FOTO_PORTADA'])

        contexto = {
            'usuario': usuario,
            'foto_perfil': url_perfil,
            'foto_portada': url_portada
        }

        return render(request, 'editar_perfil.html', contexto)

    if request.method == 'POST':
        data = {
            'NOMBRE': request.POST.get('nombre'),
            'APELLIDO': request.POST.get('apellido'),
            'CORREO': request.POST.get('correo'),
            'CONTRASENA': request.POST.get('contrasena'),
            'INTERESES': request.POST.getlist('intereses[]'),  # <- importante
        }

        archivos = {}
        if request.FILES.get('FOTO_PERFIL'):
            archivos['FOTO_PERFIL'] = request.FILES['FOTO_PERFIL']
        if request.FILES.get('FOTO_PORTADA'):
            archivos['FOTO_PORTADA'] = request.FILES['FOTO_PORTADA']

        response = actualizar_usuario(request, data, archivos)
        if response and response.ok:
            usuario_actualizado = response.json().get('usuario')
            if usuario_actualizado:
                request.session['usuario'] = usuario_actualizado
            return redirect('Perfil')
        else:
            error = "Error al actualizar el perfil"
            try:
                error = response.json().get('error', error)
            except Exception:
                pass
            return redirect('Perfil')