from bd.proyecto import (
    obtener_etiquetas, crear_etiqueta,
    obtener_integrantes_proyecto, crear_integrante,
    obtener_postulaciones, crear_postulacion,
    obtener_proyectos, crear_proyecto,
    obtener_proyecto_etiqueta, crear_proyecto_etiqueta
)
from config import table_url, headerApi
import requests

def list_etiquetas(): return obtener_etiquetas()

def add_etiqueta(data): return crear_etiqueta(data)

def list_integrantes(): return obtener_integrantes_proyecto()

def add_integrante(data): return crear_integrante(data)

def list_postulaciones(): return obtener_postulaciones()

def add_postulacion(data): return crear_postulacion(data)

def validar_proyecto(data):
    errores = []
    if not data.get('ID_USUARIO'):
        errores.get('Error al encontrar propietario de proyecto.')
    if not data.get('TITULO'):
        errores.get('El Titulo es obligatorio')
    if not data.get('NOMBRE_PROYECTO'):
        errores.get('El Nombre es obligatorio')
    if not data.get('DESCRIPCION'):
        errores.get('La descripción es obligatoria')
    if not data.get('FECHA_INICIO'):
        errores.get('Error al cargar fecha de inicio.')
    if not data.get('DURACION'):
        errores.get('Agregar Duración de proyecto es obligatorio.')
    if not data.get('ID_SEDE'):
        errores.get('Error al encontrar SEDE del usuario.')
    if not data.get('REQUISITOS'):
        errores.get('Los requisitos son obligatorios')
    if not data.get('CARRERA_DESTINO'):
        errores.get('Error al encontrar carrera destino.')
    if not data.get('FOTO_PROYECTO'):
        errores.get('La Foto de proyecto es obligatoria.')
    if not data.get('ESTADO'):
        errores.get('El Estado es obligatorio')

    return errores


def list_proyectos(): return obtener_proyectos()

def add_proyecto(data): 
    try:
        errores = validar_proyecto(data)
        if errores:
            return {'ok':False, 'errores':errores},400
        resp = crear_proyecto(data)
        if resp.ok:
            return {'mensaje':'Proyecto creado correctamente.'}, 400
        else:
            try:
                error_msg = resp.json().get('error','Error desconocido al crear proyecto.')
            except Exception:
                error_msg = resp.text
            return {'error':error_msg}, resp.status_code
    except Exception as e:
        return {'error': f'Excepción interna: {str(e)}'}, 500  
    
    
    
    
    

def list_proyecto_etiqueta():
    proyecto_etiqueta_data = requests.get(table_url('PROYECTO_ETIQUETA'),headers=headerApi()).json()
    proyectos = requests.get(table_url('PROYECTO'), headers=headerApi()).json()
    etiquetas = requests.get(table_url('ETIQUETA'), headers=headerApi()).json()

    dict_proyectos = {s['ID_PROYECTO']:s['NOMBRE_PROYECTO'] for s in proyectos}
    dict_etiquetas = {s['ID_ETIQUETA']:s['NOMBRE'] for s in etiquetas}

    for item in proyecto_etiqueta_data:
        item['PROYECTO'] = dict_proyectos.get(item['ID_PROYECTO'],'Desconocida')
        item['ETIQUETA'] = dict_etiquetas.get(item['ID_ETIQUETA'], 'Desconocida')

        
    return proyecto_etiqueta_data
    
    
    
    
    return obtener_proyecto_etiqueta()

def add_proyecto_etiqueta(data): return crear_proyecto_etiqueta(data)