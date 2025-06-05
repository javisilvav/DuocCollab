import os, uuid
from config import UPLOAD_FOLDER, allowed_file, ALLOWED_EXTENSIONS



def validar_carga_img(imagen, nombre_campo='Imagen'):
    errores = []
    if not imagen:
        errores.append(f'{nombre_campo}: No se ha subido ninguna imagen.')
        return errores
    tipos_permitidos = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/jpg']
    print(imagen)
    print(imagen.content_type)
    if imagen.content_type not in tipos_permitidos:
        errores.append(f'{nombre_campo}: El tipo de archivo no es válido. Solo se permiten {ALLOWED_EXTENSIONS}')
    # Calcular tamaño del archivo correctamente
    pos_actual = imagen.stream.tell()
    imagen.stream.seek(0, 2)
    tamano = imagen.stream.tell()
    imagen.stream.seek(pos_actual)
    if tamano > 2 * 1024 * 1024:
        errores.append(f'{nombre_campo}: El archivo es demasiado grande. Máximo 2MB.')
    return errores


def guardar_imagen(tipo, archivo):
    

    if archivo and allowed_file(archivo.filename):
        ext = archivo.filename.rsplit('.', 1)[1].lower()
        nuevo_nombre = f"{uuid.uuid4().hex}.{ext}"
        ruta_directorio = os.path.join(UPLOAD_FOLDER, 'proyecto', tipo)
        os.makedirs(ruta_directorio, exist_ok=True)
        ruta_completa = os.path.join(ruta_directorio, nuevo_nombre)
        archivo.save(ruta_completa)
        return nuevo_nombre
    return None


def trae_ruta_imagen(tipo):
    return os.path.join(UPLOAD_FOLDER,'proyecto', tipo)