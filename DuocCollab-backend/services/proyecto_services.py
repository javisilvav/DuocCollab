from bd.supabase_client import supabase
from datetime import datetime
from datetime import date
from .proyecto_consistencia import validar_carga_img, guardar_imagen

def obtener_proyecto_usuario(id_usuario):
    try:

        resultado = supabase.table("PROYECTO").select("*,SEDE(NOMBRE_SEDE), PROYECTO_ETIQUETA(ETIQUETA(NOMBRE)) , INTEGRANTES_PROYECTO(ROL, USUARIO(NOMBRE, APELLIDO)), POSTULACION(*,USUARIO(NOMBRE, APELLIDO, CORREO))").eq("ID_USUARIO", id_usuario).execute()
        if resultado.data:
            proyectos = resultado.data
            for proyecto in proyectos:
                if "POSTULACION" in proyecto:
                    proyecto["POSTULACION"] = [
                        p for p in proyecto["POSTULACION"]
                        if p.get("ESTADO") not in ["Rechazada","Cancelada"]
                    ]

            return proyectos, 200
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
        resultado = supabase.table("PROYECTO").select("*,SEDE(NOMBRE_SEDE)").execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Proyectos no encontrados."}, 404
    except Exception as e:
        return {"error": f"Error al consultar los proyectos: {str(e)}"}, 500


def editar_estado_proyecto(datos):
    try:
        id_proyecto = datos.get('ID_PROYECTO')
        estado = datos.get('ESTADO')
        resultado = supabase.table("PROYECTO").update({"ESTADO":estado}).eq("ID_PROYECTO",id_proyecto).execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Proyecto no encontrada."}, 404
    except Exception as e:
        return {"error": f"Error al modificar el estado de proyecto del usuario: {str(e)}"}, 500
    






def obtener_integrante_proyecto():
    try:

        resultado = supabase.table("PROYECTO").select("*, INTEGRANTES_PROYECTO(ROL, USUARIO(NOMBRE, APELLIDO))").execute()
        if resultado.data:
            proyectos = resultado.data

            return proyectos, 200
        else:
            return {"error": "Proyectos e integrantes no encontrado."}, 404
    except Exception as e:
        return {"error": f"Error al consultar proyectos e integrantes: {str(e)}"}, 500










def cargar_proyecto(id_usuario, datos_proyecto, archivo_imagen):
    errores = []
    campos_obligatorios = ['TITULO', 'NOMBRE_PROYECTO', 'DESCRIPCION',
                           'DURACION', 'ID_SEDE', 'REQUISITOS', 'CARRERA_DESTINO']
    



    for campo in campos_obligatorios:
        if campo not in datos_proyecto or not datos_proyecto[campo][0].strip():
            errores.append(f'{campo}: Campo obligatorio.')

    if not archivo_imagen:
        errores.append('FOTO_PROYECTO: Imagen obligatoria.')
    else:
        errores += validar_carga_img(archivo_imagen, 'FOTO_PROYECTO')

    if errores:
        return {'error': errores}, 400

    nombre_imagen = guardar_imagen('proyecto', archivo_imagen)


    try:
        nuevo_proyecto = {
            "ID_USUARIO": id_usuario,
            "TITULO": datos_proyecto['TITULO'][0],
            "NOMBRE_PROYECTO": datos_proyecto['NOMBRE_PROYECTO'][0],
            "DESCRIPCION": datos_proyecto['DESCRIPCION'][0],
            "FECHA_INICIO": date.today().isoformat(),
            "DURACION": datos_proyecto['DURACION'][0],
            "ID_SEDE": datos_proyecto['ID_SEDE'][0],
            "REQUISITOS": datos_proyecto['REQUISITOS'][0],
            "CARRERA_DESTINO": datos_proyecto['CARRERA_DESTINO'][0],
            "FOTO_PROYECTO": nombre_imagen,
            "ESTADO": 1
        }
        
        respuesta = supabase.table("PROYECTO").insert(nuevo_proyecto).execute() 
        nuevo_id_proyecto = respuesta.data[0]['ID_PROYECTO']  

        for i in datos_proyecto['INTERESES']:
            datos = {"ID_PROYECTO":nuevo_id_proyecto,"ID_ETIQUETA":int(i)}
            supabase.table("PROYECTO_ETIQUETA").insert(datos).execute() 


        for i in datos_proyecto['COLABORADOR']:
            resultado = supabase.table("USUARIO").select("ID_USUARIO").eq("CORREO",i).execute()
            if resultado.data:
                print(resultado.data[0]["ID_USUARIO"])
                colaboradores = {"ID_USUARIO": resultado.data[0]["ID_USUARIO"], "ID_PROYECTO":nuevo_id_proyecto,"ROL":'Sin rol especificado'}
                supabase.table("INTEGRANTES_PROYECTO").insert(colaboradores).execute() 
                
        return {"mensaje": "Proyecto creado correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al crear proyecto: {str(e)}"}, 500
    

def editar_proyecto(datos_proyecto, archivo_imagen=None):
    errores = []
    campos_obligatorios = ['TITULO', 'NOMBRE_PROYECTO', 'DESCRIPCION',
                           'DURACION', 'ID_SEDE', 'REQUISITOS', 'CARRERA_DESTINO']
    

    for campo in campos_obligatorios:
        if campo not in datos_proyecto or not datos_proyecto[campo][0].strip():
            errores.append(f'{campo}: Campo obligatorio.')

    if archivo_imagen:
        errores += validar_carga_img(archivo_imagen, 'FOTO_PROYECTO')

    id_proyecto = datos_proyecto['ID_PROYECTO'][0]
    if not id_proyecto:
        errores.append('Falta ID del proyecto.')

    if errores:
        return {'errores': errores}, 400
    

    try:
        # Traer imagen anterior si no se subió una nueva
        if archivo_imagen:
            nombre_imagen = guardar_imagen('proyecto', archivo_imagen)
        else:
            
            resultado = supabase.table("PROYECTO").select("FOTO_PROYECTO").eq("ID_PROYECTO", id_proyecto).execute()
            if not resultado.data:
                return {"errores": "Proyecto no encontrado."}, 404
            nombre_imagen = resultado.data[0]["FOTO_PROYECTO"]

        datos_actualizados = {
            "TITULO": datos_proyecto['TITULO'][0],
            "NOMBRE_PROYECTO": datos_proyecto['NOMBRE_PROYECTO'][0],
            "DESCRIPCION": datos_proyecto['DESCRIPCION'][0],
            "DURACION": datos_proyecto['DURACION'][0],
            "ID_SEDE": datos_proyecto['ID_SEDE'][0],
            "REQUISITOS": datos_proyecto['REQUISITOS'][0],
            "CARRERA_DESTINO": datos_proyecto['CARRERA_DESTINO'][0],
            "FOTO_PROYECTO": nombre_imagen,
        }

        supabase.table("PROYECTO").update(datos_actualizados).eq("ID_PROYECTO", id_proyecto).execute()

        ## Actualizar INTERESES
        #supabase.table("PROYECTO_ETIQUETA").delete().eq("ID_PROYECTO", id_proyecto).execute()
        #for i in datos_proyecto.get('INTERESES', []):
        #    supabase.table("PROYECTO_ETIQUETA").insert({
        #        "ID_PROYECTO": id_proyecto,
        #        "ID_ETIQUETA": int(i)
        #    }).execute()
#
        ## Actualizar COLABORADORES
        #supabase.table("INTEGRANTES_PROYECTO").delete().eq("ID_PROYECTO", id_proyecto).execute()
        #for correo in datos_proyecto.get('COLABORADOR', []):
        #    resultado = supabase.table("USUARIO").select("ID_USUARIO").eq("CORREO", correo).execute()
        #    if resultado.data:
        #        colaborador_id = resultado.data[0]["ID_USUARIO"]
        #        supabase.table("INTEGRANTES_PROYECTO").insert({
        #            "ID_USUARIO": colaborador_id,
        #            "ID_PROYECTO": id_proyecto,
        #            "ROL": "Sin rol especificado"
        #        }).execute()
#
        return {"mensaje": "Proyecto actualizado correctamente."}, 201

    except Exception as e:
        return {"errores": f"Error al actualizar proyecto: {str(e)}"}, 500





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
        print(resultado)
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
    



def obtener_postulaciones():
    try:
        resultado = supabase.table("POSTULACION").select('*,PROYECTO(NOMBRE_PROYECTO,TITULO, FOTO_PROYECTO,USUARIO(NOMBRE,APELLIDO))').execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Postulaciones no encontrado."}, 404
    except Exception as e:
        return {"error": f"Error al consultar las postulaciones: {str(e)}"}, 500




def obtener_etiquetas():
    try:
        resultado = supabase.table("ETIQUETA").select("*").execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Etiquetas no encontradas."}, 404
    except Exception as e:
        return {"error": f"Error al consultar los etiquetas: {str(e)}"}, 500
    


def cargar_etiqueta(datos):
    errores = []
    nombre_etiqueta = datos.get('nombre_etiqueta')
    if not nombre_etiqueta or not str(nombre_etiqueta).strip():
        errores.append('Nombre etiqueta: Campo obligatorio.')

    if errores:
        return {"error": errores}, 400 

    nueva_etiqueta = {
        "NOMBRE": nombre_etiqueta
    }

    try:
        supabase.table("ETIQUETA").insert(nueva_etiqueta).execute()
        return {"mensaje": "Etiqueta registrada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al registrar la etiqueta: {str(e)}"}, 500



def editar_etiqueta(datos):
    try:
        id = datos.get('id')
        nombre = datos.get('nueva_etiqueta')
        resultado = supabase.table("ETIQUETA").update({"ID_ETIQUETA":id, "NOMBRE":nombre}).eq("ID_ETIQUETA",id).execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Etiqueta no encontrada."}, 404
    except Exception as e:
        return {"error": f"Error al modificar etiqueta: {str(e)}"}, 500




def obtener_proyecto_etiqueta():
    try:
        resultado = supabase.table("PROYECTO_ETIQUETA").select("*, PROYECTO(ID_PROYECTO, NOMBRE_PROYECTO), ETIQUETA(ID_ETIQUETA, NOMBRE)").execute()
        if resultado.data:
            return resultado.data, 200
        else:
            return {"error": "Etiquetas no encontradas."}, 404
    except Exception as e:
        return {"error": f"Error al consultar los etiquetas: {str(e)}"}, 500

def cargar_proyecto_etiqueta(datos):
    errores = []
    etiqueta = datos.get('etiqueta')
    proyecto = datos.get('proyecto')
    if not etiqueta or not str(etiqueta).strip():
        errores.append('Etiqueta: Campo obligatorio.')
    if not proyecto or not str(proyecto).strip():
        errores.append('Proyecto: Campo obligatorio.')

    if errores:
        return {"error": errores}, 400 

    nuevo_proyecto_etiqueta = {
        "ID_ETIQUETA": etiqueta,
        "ID_PROYECTO": proyecto
    }
    print(nuevo_proyecto_etiqueta)

    try:
        supabase.table("PROYECTO_ETIQUETA").insert(nuevo_proyecto_etiqueta).execute()
        return {"mensaje": "Proyecto y etiqueta relacionada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al relacionar proyecto y etiqueta: {str(e)}"}, 500    



def actualizar_proyecto_etiqueta(datos):
    id = datos.get('id')
    nuevo_proyecto = datos.get('nuevo_proyecto')
    nueva_etiqueta = datos.get('nueva_etiqueta')

    if not id:
        return {'errores': 'ID tabla: Campo obligatorio.'}, 400
    if not nuevo_proyecto:
        return {'errores': 'ID sede: Campo obligatorio.'}, 400
    if not nueva_etiqueta:
        return {'errores': 'ID escuela: Campo obligatorio.'}, 400
    
    try:
        query = supabase.table("PROYECTO_ETIQUETA").update({'ID_PROYECTO':nuevo_proyecto,'ID_ETIQUETA':nueva_etiqueta}).eq("ID_TABLA",id).execute()
        if query.data == []:
            return {'errores':f'No se encontraron las ID: {id}'},404
        return {'mensaje':'Etiqueta de proyecto actualizada correctamente.'},200
    except Exception as e:
        return {'error':f'Error al actualizar etiqueta de proyecto: {str(e)}'},500
    





def contar_proyectos():
    try:       
        resultado = supabase.table('PROYECTO').select('ID_PROYECTO', count='exact').eq("ESTADO",'TRUE').execute()
        if resultado.count:
            return {"total":resultado.count}, 200
        else:
            return {'error':f'No se encontró cantidad de proyectos activos.'},404
    except Exception as e:
        return {'error':f'Error al consultar cantidad de proyectos activos'},500
    


def contar_postulacion_pendiente():
    try:       
        resultado = supabase.table('POSTULACION').select('ID_POSTULACION', count='exact').eq("ESTADO",'Solicitado').execute()
        if resultado.count:
            return {"total":resultado.count}, 200
        else:
            return {'error':f'No se encontró cantidad de postulaciones pendientes.'},404
    except Exception as e:
        return {'error':f'Error al consultar cantidad de postulaciones pendientes.'},500