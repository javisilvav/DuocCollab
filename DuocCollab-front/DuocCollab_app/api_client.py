import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = 'http://127.0.0.1:5050/api/'

# FUNCIONES AUXILIARES
def headers_auth(request):
    token = request.session.get('jwt_token')
    if not token:
        raise Exception("Token no encontrado en sesión")
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

# IMÁGENES
def trae_img_perfil(perfil, portada):
    url_perfil = f'{BASE_API_URL}uploads/imagenes/{perfil}'
    url_portada = f'{BASE_API_URL}uploads/imagenes/{portada}'
    return url_perfil, url_portada

def trae_img_proyecto(proyecto):
    return f'{BASE_API_URL}uploads/imagenes_proyecto/{proyecto}'

# AUTENTICACIÓN
def iniciar_sesion(correo, contrasenia):
    response = requests.post(
        f'{BASE_API_URL}login',
        json={'CORREO': correo, 'CONTRASENIA': contrasenia}
    )
    return response.json()

# CONSULTAS VARIAS (con headers JWT)
def consulta_sede(request):
    try:
        response = requests.get(f'{BASE_API_URL}sedes', headers=headers_auth(request))
        if response.ok:
            return response.json()
        else:
            print(f'Error en la API: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Token inválido o ausente: {e}')
    return []

def consulta_carrera(request):
    try:
        response = requests.get(f'{BASE_API_URL}carreras', headers=headers_auth(request))
        if response.ok:
            return response.json()
        else:
            print(f'Error en la API: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Token inválido o ausente: {e}')
    return []

def consulta_escuela(request):
    try:
        response = requests.get(f'{BASE_API_URL}escuelas', headers=headers_auth(request))
        if response.ok:
            return response.json()
        else:
            print(f'Error en la API: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Token inválido o ausente: {e}')
    return []

def consulta_proyectos(request):
    try:
        response = requests.get(f'{BASE_API_URL}proyectos', headers=headers_auth(request))
        if response.ok:
            return response.json()
        else:
            print(f'Error en la API: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Token inválido o ausente: {e}')
    return []


def consulta_mis_proyectos(request):
    try:
        response = requests.get(f'{BASE_API_URL}mis-proyectos', headers=headers_auth(request))
        if response.ok:
            return response.json()
        else:
            print(f'Error en la API: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Token inválido o ausente: {e}')
    return []


def consulta_mis_postulaciones(request):
    try:
        response = requests.get(f'{BASE_API_URL}mis-postulaciones', headers=headers_auth(request))
        if response.ok:
            return response.json()
        else:
            print(f'Error en la API: {response.status_code} - {response.text}')
    except Exception as e:
        print(f'Token inválido o ausente: {e}')
    return []

# REGISTRO DE USUARIOS
def registrar_usuario(request, data, archivos=None):
    try:
        headers = headers_auth(request)
        headers.pop('Content-Type', None)  # Para permitir multipart/form-data
        response = requests.post(
            f'{BASE_API_URL}usuarios',
            data=data,
            files=archivos,
            headers=headers
        )
        return response
    except Exception as e:
        print(f'Error al registrar usuario: {e}')
        return None
