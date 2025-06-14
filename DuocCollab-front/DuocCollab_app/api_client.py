import requests
import os
from dotenv import load_dotenv
from requests import request


load_dotenv()
API_URL = 'http://127.0.0.1:5050/api'
#API_TOKEN=os.getenv('API_TOKEN')


def api_request(method, endpoint, token=None, **kwargs):
    headers = kwargs.pop('headers',{})
    if token:
        headers['Authorization'] = f'Bearer {token}'
    try:
        response = requests.request(method,f'{API_URL}{endpoint}',headers=headers,**kwargs)
        
        if response.status_code == 401 and endpoint not in ['/auth/login', '/auth/registro']:
            return {'expired': True, 'message': 'Sesión expirada, favor iniciar sesión nuevamente'}
        return {'expired': False,'response':response}
    except requests.exceptions.RequestException as e:
        return {'expired':False,'error':f'Error de conexión: {str(e)}'}




def ruta_img_perfil_portada(perfil, portada):
    img_perfil = f'{API_URL}/auth/imagen/perfil/{perfil}'
    print(img_perfil)
    img_portada = f'{API_URL}/auth/imagen/portada/{portada}'
    return img_perfil, img_portada

def ruta_img_proyecto(img):
    img_proyecto = f'{API_URL}/proyecto/imagen/proyecto/{img}'
    return img_proyecto









#
#def trae_img_perfil(perfil, portada):
#
#    url_perfil = f'{BASE_API_URL}uploads/imagenes/{perfil}'
#    url_portada = f'{BASE_API_URL}uploads/imagenes/{portada}'
#
#    return url_perfil, url_portada
#
#
#
#
#    
#


#
#    
#def consulta_escuela():
#    response = requests.get(f'{BASE_API_URL}escuelas', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#
#def consulta_escuela():
#    response = requests.get(f'{BASE_API_URL}escuelas', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#
#def consulta_sede_escuela():
#    response = requests.get(f'{BASE_API_URL}sedeEscuela', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#def consulta_etiqueta():
#    response = requests.get(f'{BASE_API_URL}etiquetas', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#def consulta_usuario():
#    response = requests.get(f'{BASE_API_URL}usuarios', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#def consulta_proyecto():
#    response = requests.get(f'{BASE_API_URL}proyectos', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#def consuta_proyecto_etiqueta():
#    response = requests.get(f'{BASE_API_URL}proyectoEtiqueta', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#def consulta_integrantes():
#    response = requests.get(f'{BASE_API_URL}integrantesProyectos', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []
#    
#def consulta_postulacion():
#    response = requests.get(f'{BASE_API_URL}postulantes', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []