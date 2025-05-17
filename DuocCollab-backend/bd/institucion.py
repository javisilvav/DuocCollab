import json
import requests
from config import table_url, headerApi

# Tablas: SEDE, CARRERA, ESCUELA, SEDE_ESCUELA

def obtener_sedes():
    resp = requests.get(table_url('SEDE'), headers=headerApi())
    return resp.json() if resp.ok else []

def crear_sede(data: dict) -> requests.Response:
    return requests.post(
        table_url('SEDE'),
        headers=headerApi(),
        data=json.dumps({'NOMBRE_SEDE': data['NOMBRE_SEDE']})
    )




def obtener_carreras():
    resp = requests.get(table_url('CARRERA'), headers=headerApi())
    return resp.json() if resp.ok else []

def crear_carrera(data: dict) -> requests.Response:
    return requests.post(
        table_url('CARRERA'),
        headers=headerApi(),
        data=json.dumps({
            'NOMBRE': data['NOMBRE'],
            'ID_ESCUELA': data['ID_ESCUELA']
        })
    )

def obtener_escuelas():
    resp = requests.get(table_url('ESCUELA'), headers=headerApi())
    return resp.json() if resp.ok else []

def crear_escuela(data: dict) -> requests.Response:
    return requests.post(
        table_url('ESCUELA'),
        headers=headerApi(),
        data=json.dumps({'NOMBRE_ESC': data['NOMBRE_ESC']})
    )

def obtener_sede_escuela():
    sede_escuela_data = requests.get(table_url('SEDE_ESCUELA'), headers = headerApi()).json()
    sedes = requests.get(table_url('SEDE'), headers=headerApi()).json()
    escuelas = requests.get(table_url('ESCUELA'), headers=headerApi()).json()

    dict_sedes = {s['ID_SEDE']: s['NOMBRE_SEDE'] for s in sedes}
    dict_escuelas = {s['ID_ESCUELA']: s['NOMBRE_ESC'] for s in escuelas}

    for item in sede_escuela_data:
        item['SEDE'] = dict_sedes.get(item['ID_SEDE'], 'Desconocida')
        item['ESCUELA'] = dict_escuelas.get(item['ID_ESCUELA'], 'Desconocida')

    return sede_escuela_data

def crear_sede_escuela(data: dict) -> requests.Response:
    return requests.post(
        table_url('SEDE_ESCUELA'),
        headers=headerApi(),
        data=json.dumps({
            'ID_SEDE': data['ID_SEDE'],
            'ID_ESCUELA': data['ID_ESCUELA']
        })
    )




