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
        errores.append('Error al encontrar propietario de proyecto.')
    if not data.get('TITULO'):
        errores.append('El Titulo es obligatorio')
    if not data.get('NOMBRE_PROYECTO'):
        errores.append('El Nombre es obligatorio')
    if not data.get('DESCRIPCION'):
        errores.append('La descripción es obligatoria')
    if not data.get('FECHA_INICIO'):
        errores.append('Error al cargar fecha de inicio.')
    if not data.get('DURACION'):
        errores.append('Agregar Duración de proyecto es obligatorio.')
    if not data.get('ID_SEDE'):
        errores.append('Error al encontrar SEDE del usuario.')
    if not data.get('REQUISITOS'):
        errores.append('Los requisitos son obligatorios')
    if not data.get('CARRERA_DESTINO'):
        errores.append('Error al encontrar carrera destino.')
    if not data.get('FOTO_PROYECTO'):
        errores.append('La Foto de proyecto es obligatoria.')
    if not data.get('ESTADO'):
        errores.append('El Estado es obligatorio')

    return errores


def list_proyectos(): return obtener_proyectos()

def obtener_proyectos_por_usuario(id_usuario):
    todos = obtener_proyectos()
    filtrados = [p for p in todos if str(p.get('ID_USUARIO')) == str(id_usuario)]
    return filtrados

def obtener_postulaciones_por_usuario(id_usuario):
    todos = obtener_postulaciones()
    filtrados = [p for p in todos if str(p.get('ID_USUARIO')) == str(id_usuario)]
    return filtrados




def add_proyecto(data): 
    try:
        errores = validar_proyecto(data)
       
        if errores:
            return {'ok':False, 'errores':errores},400
        resp = crear_proyecto(data)
        if resp.ok:
            return {'mensaje':'Proyecto creado correctamente.'}, 201
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
    
    
    


def add_proyecto_etiqueta(data): return crear_proyecto_etiqueta(data)