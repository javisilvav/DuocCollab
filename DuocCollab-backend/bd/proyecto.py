import json
import requests
from config import table_url, headerApi

# Tablas: ETIQUETA, INTEGRANTES_PROYECTO, POSTULACION, PROYECTO, PROYECTO_ETIQUETA

def obtener_etiquetas():
    resp = requests.get(table_url('ETIQUETA'), headers=headerApi())
    return resp.json() if resp.ok else []

def crear_etiqueta(data: dict) -> requests.Response:
    return requests.post(
        table_url('ETIQUETA'),
        headers=headerApi(),
        data=json.dumps({'NOMBRE': data['NOMBRE']})
    )

def obtener_integrantes_proyecto():
    integrantes_proyectos = requests.get(table_url('INTEGRANTES_PROYECTO'), headers=headerApi()).json()
    integrantes = requests.get(table_url('USUARIO'), headers = headerApi()).json()
    proyectos = requests.get(table_url('PROYECTO'),headers=headerApi()).json()

    dict_integrantes = {s['ID_USUARIO']: f"{s['NOMBRE']} {s['APELLIDO']}" for s in integrantes}
    dict_proyecto = {s['ID_PROYECTO']: s['NOMBRE_PROYECTO']for s in proyectos}

    for item in integrantes_proyectos:
        item['USUARIO'] = dict_integrantes.get(item['ID_USUARIO'],'Desconocida')
        item['PROYECTO'] = dict_proyecto.get(item['ID_PROYECTO'], 'Desconocida')

        
    return integrantes_proyectos

def crear_integrante(data: dict) -> requests.Response:
    return requests.post(
        table_url('INTEGRANTES_PROYECTO'),
        headers=headerApi(),
        data=json.dumps({
            'ID_USUARIO': data['ID_USUARIO'],
            'ID_PROYECTO': data['ID_PROYECTO'],
            'ROL': data['ROL']
        })
    )

def obtener_postulaciones():
    resp = requests.get(table_url('POSTULACION'), headers=headerApi())

    
    return resp.json() if resp.ok else []

def crear_postulacion(data: dict) -> requests.Response:
    return requests.post(
        table_url('POSTULACION'),
        headers=headerApi(),
        data=json.dumps({
            'ID_USUARIO': data['ID_USUARIO'],
            'ID_PROYECTO': data['ID_PROYECTO'],
            'FECHA_POSTULACION': data['FECHA_POSTULACION'],
            'FECHA_RESOLUCION': data['FECHA_RESOLUCION'],
            'ESTADO': data['ESTADO']
        })
    )

def obtener_proyectos():
    proyectos_data = requests.get(table_url('PROYECTO'), headers=headerApi()).json()
    propietario = requests.get(table_url('USUARIO'), headers = headerApi()).json()
    sedes = requests.get(table_url('SEDE'), headers=headerApi()).json()

    dict_propietario = {s['ID_USUARIO']: f"{s['NOMBRE']} {s['APELLIDO']}" for s in propietario}
    dict_sedes = {s['ID_SEDE']: s['NOMBRE_SEDE'] for s in sedes}

    for item in proyectos_data:
        item['USUARIO'] = dict_propietario.get(item['ID_USUARIO'], 'Desconocida')
        item['SEDE'] = dict_sedes.get(item['ID_SEDE'],'Desconocida')

    return proyectos_data




def crear_proyecto(data: dict) -> requests.Response:
    payload = {
        'ID_USUARIO': data['ID_USUARIO'],
        'TITULO': data['TITULO'],
        'NOMBRE_PROYECTO': data['NOMBRE_PROYECTO'],
        'DESCRIPCION': data['DESCRIPCION'],
        'FECHA_INICIO': data['FECHA_INICIO'],
        'DURACION': data['DURACION'],
        'ID_SEDE': data['ID_SEDE'],
        'REQUISITOS': data['REQUISITOS'],
        'CARRERA_DESTINO': data['CARRERA_DESTINO'],
        'FOTO_PROYECTO': data['FOTO_PROYECTO'],
        'ESTADO': data['ESTADO']
    }
    return requests.post(table_url('PROYECTO'), headers=headerApi(), data=json.dumps(payload))
    

def obtener_proyecto_etiqueta():
    resp = requests.get(table_url('PROYECTO_ETIQUETA'), headers=headerApi())
    return resp.json() if resp.ok else []

def crear_proyecto_etiqueta(data: dict) -> requests.Response:
    return requests.post(
        table_url('PROYECTO_ETIQUETA'),
        headers=headerApi(),
        data=json.dumps({
            'ID_PROYECTO': data['ID_PROYECTO'],
            'ID_ETIQUETA': data['ID_ETIQUETA']
        })
    )