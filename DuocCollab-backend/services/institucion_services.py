from bd.supabase_client import supabase


def obtener_sede_escuela():
    relaciones = supabase.table('SEDE_ESCUELA').select('*').execute().data
    resultado = []
    for rel in relaciones:
        sede = supabase.table('SEDE').select('NOMBRE_SEDE').eq('ID_SEDE', rel['ID_SEDE']).execute().data
        escuela = supabase.table('ESCUELA').select('NOMBRE_ESC').eq('ID_ESCUELA', rel['ID_ESCUELA']).execute().data
        resultado.append({
            "ID_tabla":rel['ID_tabla'],
            "ID_SEDE": rel['ID_SEDE'],
            "ID_ESCUELA":rel['ID_ESCUELA'],
            "NOMBRE_SEDE": sede[0]['NOMBRE_SEDE'] if sede else None,
            "NOMBRE_ESC": escuela[0]['NOMBRE_ESC'] if escuela else None
        })
    return resultado



def cargar_sd_esc(datos):
    id_sede = datos.get('id_sede')
    id_escuela = datos.get('id_escuela')
    if not id_sede:
        return {'errores': 'Nombre sede: Campo obligatorio.'}, 400
    if not id_escuela:
        return {'errores': 'Nombre escuela: Campo obligatorio.'}, 400
    try:
        nuevo = {
            'ID_SEDE': id_sede,
            'ID_ESCUELA': id_escuela
            }
        supabase.table("SEDE_ESCUELA").insert(nuevo).execute()
        return {"mensaje": "Sede y Escuela relacionada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al relacionar sede y escuela: {str(e)}"}, 500

def actualizar_sd_esc(datos):
    id = datos.get('id')
    nueva_sede = datos.get('nueva_sede')
    nueva_escuela = datos.get('nueva_escuela')

    if not id:
        return {'errores': 'ID sede: Campo obligatorio.'}, 400
    if not nueva_sede:
        return {'errores': 'ID sede: Campo obligatorio.'}, 400
    if not nueva_escuela:
        return {'errores': 'ID escuela: Campo obligatorio.'}, 400
    
    try:
        query = supabase.table("SEDE_ESCUELA").update({'ID_SEDE':nueva_sede,'ID_ESCUELA':nueva_escuela}).eq("ID_tabla",id).execute()
        if query.data == []:
            return {'errores':f'No se encontraron las ID: {id}'},404
        return {'mensaje':'Sede y escuela actualizada correctamente.'},200
    except Exception as e:
        return {'error':f'Error al actualizar sede y escuela: {str(e)}'},500






def obtener_escuelas():
    try:
        return supabase.table('ESCUELA').select('*').execute().data, 200
    except:
        return {'error':'No se lograron cargar las escuelas.'},500
    

def cargar_escuela(datos):
    nombre = datos['nombre_escuela'].strip()
    if not nombre:
        return {'errores': 'Nombre escuela: Campo obligatorio.'}, 400
    try:
        nuevo = {'NOMBRE_ESC': nombre}
        supabase.table("ESCUELA").insert(nuevo).execute()
        return {"mensaje": "Escuela creada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al crear escuela: {str(e)}"}, 500

def actualizar_escuela(datos):
    id = datos.get('id')
    nuevo_nombre = datos.get('nombre_escuela','').strip()

    if not id:
        return {'errores':'ID: Campo obligatorio'}, 400
    if not nuevo_nombre:
        return {'errores':'Nombre escuela: Campo obligatorio.'},400
    
    try:
        query = supabase.table("ESCUELA").update({'NOMBRE_ESC':nuevo_nombre}).eq("ID_ESCUELA",id).execute()
        if query.data == []:
            return {'errores':f'No se encontró escuela con ID: {id}'},404
        return {'mensaje':'Escuela actualizada correctamente.'},200
    except Exception as e:
        return {'error':f'Error al actualizar escuela: {str(e)}'},500


def eliminar_escuela(datos):
    id = datos.get('id')
    if not id:
        return {'errores':'ID: Campo obligatorio'}, 400

    
    try:
        id = int(id)
        query = supabase.table("ESCUELA").delete().eq("ID_ESCUELA",id).execute()
        if not query.data:
            return {'errores':f"No se encontró escuela con ID {id}."}, 404
        return {'mensaje':'Escuela eliminada correctamente.'},200
    except Exception as e:
        return {'error':f'Error al eliminar escuela: {str(e)}'},500






def obtener_carreras():
    try:
        return supabase.table('CARRERA').select('*').execute().data, 200
    except:
        return {'error':'No se lograron cargar las carreras.'},500
    

def cargar_carrera(datos):
    nombre = datos.get('nombre_carrera','').strip()
    id_escuela = datos.get('id_escuela')
    if not nombre:
        return {'errores': 'Nombre carrera: Campo obligatorio.'}, 400
    if not id_escuela:
        return {'errores':'ID escuela: Campo obligatorio'}, 400
    try:
        nuevo = {
            'NOMBRE': nombre,
            'ID_ESCUELA':id_escuela
            }
        supabase.table("CARRERA").insert(nuevo).execute()
        return {"mensaje": "Carrera creada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al crear carrera: {str(e)}"}, 500

def actualizar_carrera(datos):
    id = datos.get('id')
    nuevo_nombre = datos.get('nombre_carrera','').strip()
    id_escuela = datos.get('id_escuela')
    
    if not id:
        return {'errores':'ID: Campo obligatorio'}, 400
    if not nuevo_nombre:
        return {'errores':'Nombre carrera: Campo obligatorio.'},400
    if not id_escuela:
        return {'errores':'ID escuela: Campo obligatorio'}, 400
    
    try:
        query = supabase.table("CARRERA").update({'NOMBRE':nuevo_nombre, 'ID_ESCUELA':id_escuela}).eq("ID_CARRERA",id).execute()
        if query.data == []:
            return {'errores':f'No se encontró carrera con ID: {id}'},404
        return {'mensaje':'Carrera actualizada correctamente.'},200
    except Exception as e:
        return {'error':f'Error al actualizar carrera: {str(e)}'},500
    





def obtener_sedes():
    try:
        return supabase.table('SEDE').select('*').execute().data, 200
    except:
        return {'error':'No se lograron cargar las sedes.'},500
    

def cargar_sede(datos):
    nombre = datos.get('nombre_sede','').strip()
    if not nombre:
        return {'errores': 'Nombre sede: Campo obligatorio.'}, 400
    try:
        nuevo = {'NOMBRE_SEDE': nombre}
        supabase.table("SEDE").insert(nuevo).execute()
        return {"mensaje": "Sede creada correctamente."}, 201
    except Exception as e:
        return {"error": f"Error al crear sede: {str(e)}"}, 500

def actualizar_sede(datos):
    id = datos.get('id')
    nuevo_nombre = datos.get('nombre_sede','').strip()

    if not id:
        return {'errores':'ID: Campo obligatorio'}, 400
    if not nuevo_nombre:
        return {'errores':'Nombre sede: Campo obligatorio.'},400
    
    try:
        query = supabase.table("SEDE").update({'NOMBRE_SEDE':nuevo_nombre}).eq("ID_SEDE",id).execute()
        if query.data == []:
            return {'errores':f'No se encontró sede con ID: {id}'},404
        return {'mensaje':'Sede actualizada correctamente.'},200
    except Exception as e:
        return {'error':f'Error al actualizar sede: {str(e)}'},500

