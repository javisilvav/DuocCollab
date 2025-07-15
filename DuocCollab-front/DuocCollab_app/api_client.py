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

        try:
            data = response.json()
        except ValueError:
            data = {'error': 'La respuesta no es JSON', 'status_code': response.status_code}
        
        return {'expired':False,'status_code': response.status_code, 'response':data}
    except requests.exceptions.RequestException as e:
        return {'expired':False,'error':f'Error de conexión: {str(e)}'}




def ruta_img_perfil_portada(perfil, portada):
    img_perfil = f'{API_URL}/auth/imagen/perfil/{perfil}'
    img_portada = f'{API_URL}/auth/imagen/portada/{portada}'
    return img_perfil, img_portada

def ruta_img_proyecto(img):
    img_proyecto = f'{API_URL}/proyecto/imagen/proyecto/{img}'
    return img_proyecto




def verificar_token_y_api(token, metodo, endpoint, requiere_tkn=True,**kwargs):
    if requiere_tkn and not token:
       return 'No existe token'
    result = api_request(metodo, endpoint, token=token, **kwargs)
    if result.get('expired'):
        return 'Sesión Expirada'
    if 'error' in result:
        return result['error']

    return result



def realiza_login(datos):
    result = verificar_token_y_api('', 'POST', '/auth/login', False, json=datos, headers={'Content-Type':'application/json'})
    response = result.get('response', {})   
    return response


def realiza_recuperar_credenciales(datos):
    result = verificar_token_y_api('', 'POST', '/auth/recuperar_contrasena',False, json=datos, headers={'Content-Type': 'application/json'})
    response = result.get('response', {})
    return response

def consulta_sede():
    result = verificar_token_y_api('', 'GET', '/institucion/sedes',False)
    response = result.get('response', {})
    return response

def consulta_carrera():
    result = verificar_token_y_api('', 'GET', '/institucion/carreras',False)
    response = result.get('response', {})
    return response

def consulta_escuela():
    result = verificar_token_y_api('', 'GET', '/institucion/escuelas',False)
    response = result.get('response', {})
    return response

def realiza_nueva_cuenta(datos):
    result = verificar_token_y_api('','POST', '/auth/registro',False, json=datos, headers={'Content-Type': 'application/json'})
    response = result.get('response', {})
    return response

def consulta_usuario_actual(token):
    result = verificar_token_y_api(token,'GET', '/auth/usuario_actual')
    response = result.get('response', {})
    return response

def consulta_mis_postulaciones(token):
    result = verificar_token_y_api(token,'GET', '/proyecto/mis_postulaciones')
    response = result.get('response', {})
    return response

def consulta_mis_proyectos(token):
    result = verificar_token_y_api(token,'GET', '/proyecto/mis_proyectos')
    response = result.get('response', {})
    return response

def consulta_etiquetas(token):
    result = verificar_token_y_api(token,'GET', '/proyecto/etiquetas')
    response = result.get('response', {})
    return response

def realiza_editar_perfil(token, datos, archivos):
    result = verificar_token_y_api(token, 'PUT', '/auth/editar', data=datos, files=archivos)
    response = result.get('response', {})
    return response

def realiza_editar_postulacion(token, datos):
    result = verificar_token_y_api(token, 'POST', '/auth/editar_postulacion', data=datos, headers={'Content-Type': 'application/json'})
    response = result.get('response', {})
    return response

def realiza_editar_proyecto(token, datos, archivos):
    result = verificar_token_y_api(token, 'POST', '/proyecto/editar', data=datos, files=archivos)
    response = result.get('response', {})
    return response


def consulta_detalle_proyecto(token, datos):
    result = verificar_token_y_api(token,'GET', '/proyecto/detalle_proyecto', json=datos,headers={'Content-Type': 'application/json'})
    response = result.get('response', {})
    return response

def realiza_crear_postulacion(token, datos):
    result = verificar_token_y_api(token,'POST', '/proyecto/crear_postulacion', json=datos,headers={'Content-Type': 'application/json'})
    response = result.get('response', {})
    return response


#result = verificar_token_y_api('dsa', 'GET', '/institucion/sedes', False)
#
#print(result)



















#
#    
#def consulta_escuela():
#    response = requests.get(f'{BASE_API_URL}escuelas', headers=headers_auth())
#    if response.ok:
#        return response.json()
#    else:
#        print(f'Error en la API: {response.status_code} - {response.text}')
#        return []