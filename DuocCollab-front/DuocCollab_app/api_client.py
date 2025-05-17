import requests
import os
from dotenv import load_dotenv
from requests import request


load_dotenv()
BASE_API_URL = 'http://127.0.0.1:5050/api/'
API_TOKEN=os.getenv('API_TOKEN')

def headers_auth():
    return {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type':'application/json',
        #'X-User-ID': request.session.get('id_usuario')
    }



def trae_img_perfil(perfil, portada):

    url_perfil = f'{BASE_API_URL}uploads/imagenes/{perfil}'
    url_portada = f'{BASE_API_URL}uploads/imagenes/{portada}'

    return url_perfil, url_portada




    


def iniciar_sesion(correo, contrasenia):
    response = requests.post(
        f'{BASE_API_URL}login', 
        json={'CORREO':correo,'CONTRASENIA':contrasenia}
    )
    print(response.status_code)
    print(response.text)
    return response.json()


def consulta_sede():
    response = requests.get(f'{BASE_API_URL}sedes', headers=headers_auth())
    if response.ok:
        return response.json()
    else:
        print(f'Error en la API: {response.status_code} - {response.text}')
        return []
    
def consulta_carrera():
    response = requests.get(f'{BASE_API_URL}carreras', headers=headers_auth())
    if response.ok:
        return response.json()
    else:
        print(f'Error en la API: {response.status_code} - {response.text}')
        return []

    
def consulta_escuela():
    response = requests.get(f'{BASE_API_URL}escuelas', headers=headers_auth())
    if response.ok:
        return response.json()
    else:
        print(f'Error en la API: {response.status_code} - {response.text}')
        return []
    

def consulta_escuela():
    response = requests.get(f'{BASE_API_URL}escuelas', headers=headers_auth())
    if response.ok:
        return response.json()
    else:
        print(f'Error en la API: {response.status_code} - {response.text}')
        return []
    
def registrar_usuario(data, archivos = None):
    headers = headers_auth()
    headers.pop('Content-Type', None)
    response = requests.post(
        f'{BASE_API_URL}usuarios', 
        data=data, 
        files=archivos, 
        headers=headers
    )
    return response