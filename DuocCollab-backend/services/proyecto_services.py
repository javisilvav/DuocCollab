from bd.supabase_client import supabase
from datetime import datetime
from datetime import date
from .proyecto_consistencia import validar_carga_img, guardar_imagen

def obtener_proyecto_usuario(id_usuario):
    try:

        resultado = supabase.table("PROYECTO").select("*,SEDE(NOMBRE_SEDE), INTEGRANTES_PROYECTO(ROL, USUARIO(NOMBRE, APELLIDO)), POSTULACION(*,USUARIO(NOMBRE, APELLIDO, CORREO))").eq("ID_USUARIO", id_usuario).execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Proyectos del usuario no encontrado."}, 404
    except Exception as e:
        return {"error": f"Error al consultar proyectos del usuario: {str(e)}"}, 500

    
def obtener_detalle_proyecto(data_proyecto):
    try:
        if not data_proyecto or 'id_proyecto' not in data_proyecto: 
            return {'error': 'ID del proyecto requerido.'},400
               
        id_proyecto = int(data_proyecto['id_proyecto'])
        resultado = supabase.table("PROYECTO").select("*,SEDE(NOMBRE_SEDE), USUARIO(NOMBRE, APELLIDO), INTEGRANTES_PROYECTO(ROL, USUARIO(NOMBRE, APELLIDO))").eq("ID_PROYECTO", id_proyecto).execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Detalle del proyecto no encontrado."}, 404
    except Exception as e:
        return {"error": f"Error al consultar detalle de proyecto: {str(e)}"}, 500
    

def obtener_proyetos():
    try:
        resultado = supabase.table("PROYECTO").select("*").execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Proyectos no encontrados."}, 404
    except Exception as e:
        return {"error": f"Error al consultar los proyectos: {str(e)}"}, 500



def cargar_proyecto(id_usuario, datos_proyecto, archivo_imagen):
    errores = []
    campos_obligatorios = ['TITULO', 'NOMBRE_PROYECTO', 'DESCRIPCION',
                           'DURACION', 'ID_SEDE', 'REQUISITOS', 'CARRERA_DESTINO']

    for campo in campos_obligatorios:
        if campo not in datos_proyecto or not datos_proyecto[campo].strip():
            errores.append(f'{campo}: Campo obligatorio.')

    if not archivo_imagen:
        errores.append('FOTO_PROYECTO: Imagen obligatoria.')
    else:
        errores += validar_carga_img(archivo_imagen, 'FOTO_PROYECTO')

    if errores:
        return {'errores': errores}, 400

    nombre_imagen = guardar_imagen('proyecto', archivo_imagen)

    try:
        nuevo_proyecto = {
            "ID_USUARIO": id_usuario,
            "TITULO": datos_proyecto['TITULO'],
            "NOMBRE_PROYECTO": datos_proyecto['NOMBRE_PROYECTO'],
            "DESCRIPCION": datos_proyecto['DESCRIPCION'],
            "FECHA_INICIO": date.today().isoformat(),
            "DURACION": datos_proyecto['DURACION'],
            "ID_SEDE": datos_proyecto['ID_SEDE'],
            "REQUISITOS": datos_proyecto['REQUISITOS'],
            "CARRERA_DESTINO": datos_proyecto['CARRERA_DESTINO'],
            "FOTO_PROYECTO": nombre_imagen,
            "ESTADO": 1
        }
        supabase.table("PROYECTO").insert(nuevo_proyecto).execute()
        return {"mensaje": "Proyecto creado correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al crear proyecto: {str(e)}"}, 500
    

def cargar_postulacion(id_usuario, datos_postulacion):
    errores = []
    id_proyecto = datos_postulacion.get('ID_PROYECTO')
    comentario = datos_postulacion.get('COMENTARIO')
    if not id_proyecto or not str(id_proyecto).strip():
        errores.append('ID_PROYECTO: Campo obligatorio.')

    proyecto = supabase.table("PROYECTO").select("ID_PROYECTO").eq("ID_PROYECTO", id_proyecto).execute()
    if not proyecto.data:
        errores.append('ID_PROYECTO: Proyecto no encontrado.')

    if errores:
        return {"errores": errores}, 400 

    propietario = supabase.table("PROYECTO").select("*").eq("ID_PROYECTO", id_proyecto).eq("ID_USUARIO", id_usuario).execute()
    if propietario.data:
        return {"errores":"No puedes postular a tus proyectos."}, 409
        
    existente = supabase.table("POSTULACION").select("*").match({
        "ID_USUARIO": id_usuario,
        "ID_PROYECTO": id_proyecto
    }).execute()
    print(existente)
    if existente.data:
        return {"errores": ["Ya existe una postulación a este proyecto."]}, 409

    nueva_postulacion = {
        "ID_USUARIO": id_usuario,
        "ID_PROYECTO": id_proyecto,
        "FECHA_POSTULACION": datetime.now().isoformat(),
        "ESTADO": "Solicitado",
        "FECHA_RESOLUCION": None,
        'comentario':comentario
    }

    try:
        supabase.table("POSTULACION").insert(nueva_postulacion).execute()
        return {"mensaje": "Postulación registrada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al registrar la postulación: {str(e)}"}, 500


def obtener_postulacion_usuario(id_usuario):
    try:
        resultado = supabase.table("POSTULACION").select('*,PROYECTO(NOMBRE_PROYECTO,TITULO, FOTO_PROYECTO,USUARIO(NOMBRE,APELLIDO))').eq("ID_USUARIO", id_usuario).neq("ESTADO",'Cancelada').execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Proyectos del usuario no encontrado."}, 404
    except Exception as e:
        return {"error": f"Error al consultar proyectos del usuario: {str(e)}"}, 500
    
def editar_estado_postulacion(datos):
    try:
        id_postulacion = datos.get('ID_POSTULACION')
        estado = datos.get('ESTADO')
        resultado = supabase.table("POSTULACION").update({"ESTADO":estado, "FECHA_RESOLUCION": datetime.now().isoformat()}).eq("ID_POSTULACION",id_postulacion).execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Postulación no encontrada."}, 404
    except Exception as e:
        return {"error": f"Error al modificar postulación del usuario: {str(e)}"}, 500