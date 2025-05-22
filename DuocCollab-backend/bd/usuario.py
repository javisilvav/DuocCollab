import json
import requests
from config import table_url, headerApi
from werkzeug.security import generate_password_hash
# Tablas: USUARIO

def obtener_usuarios():
    resp = requests.get(table_url('USUARIO'), headers=headerApi()).json()
    carreras = requests.get(table_url('CARRERA'),headers=headerApi()).json()

    dict_carreras = {s['ID_CARRERA']:s['NOMBRE'] for s in carreras}

    for item in resp:
        item['CARRERA'] = dict_carreras.get(item['ID_CARRERA'],'Desconocida')

    return resp



def buscar_usuario_por_correo(correo):
    usuarios = obtener_usuarios()
    for usuario in usuarios:
        if usuario['CORREO'] == correo:
            return usuario
    return None


def crear_usuario(data: dict) -> requests.Response:
    contra = generate_password_hash(data['CONTRASENIA'])
    payload = {
        'NOMBRE': data['NOMBRE'],
        'APELLIDO': data['APELLIDO'],
        'CORREO': data['CORREO'],
        'CONTRASENIA': contra,
        'ID_CARRERA': data['ID_CARRERA'],
        'INTERESES': data.get('INTERESES'),
        'FOTO_PERFIL': data.get('FOTO_PERFIL'),
        'FOTO_PORTADA': data.get('FOTO_PORTADA')
    }
    return requests.post(table_url('USUARIO'), headers=headerApi(), data=json.dumps(payload))



def obtener_usuario_por_id(id_usuario):
    usuarios = obtener_usuarios()
    for u in usuarios:
        if u['ID_USUARIO'] == id_usuario:
            return u
    return None


def modificar_usuario(id_usuario:int, data:dict)-> requests.Response:
    payload = {
        'NOMBRE': data.get('NOMBRE'),
        'APELLIDO': data.get('APELLIDO'),
        'CORREO': data.get('CORREO'),
        'ID_CARRERA': data.get('ID_CARRERA'),
        'INTERESES': data.get('INTERESES'),
        'FOTO_PERFIL': data.get('FOTO_PERFIL'),
        'FOTO_PORTADA': data.get('FOTO_PORTADA')
    }
    if data.get('contrasena'):
        payload['CONTRASENIA'] = generate_password_hash(data['contrasena'])
    url = table_url(f'USUARIO/{id_usuario}')
    return requests.put(url, headers=headerApi(), data=json.dumps(payload))
        
