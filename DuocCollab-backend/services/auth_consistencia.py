import re
from config import UPLOAD_FOLDER, allowed_file, ALLOWED_EXTENSIONS
import os
import uuid



def guardar_imagen(tipo, archivo):
    print(archivo, 'Guardado')
    if archivo and allowed_file(archivo.filename):
        ext = archivo.filename.rsplit('.', 1)[1].lower()
        nuevo_nombre = f"{uuid.uuid4().hex}.{ext}"
        ruta_directorio = os.path.join(UPLOAD_FOLDER, 'usuario', tipo)

        os.makedirs(ruta_directorio, exist_ok=True)  # Crear carpeta si no existe

        ruta_completa = os.path.join(ruta_directorio, nuevo_nombre)
        archivo.save(ruta_completa)
        return nuevo_nombre
    return None


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

def valida_form_login(correo, clave):
    if not correo or not clave:
        return {'error':'Correo y clave son requeridos'}
    if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", correo)):
        return {'error':'Formato de correo invalido'}   
    return None

def valida_form_usuario(data,modo):
    nombre_dict = 'NOMBRE'
    apellido_dict = 'APELLIDO'
    correo_dict = 'CORREO'
    clave_dict = 'CONTRASENIA'
    sede_dict = ''
    id_carrera_dict = 'ID_CARRERA'
    escuela_dict = ''
    intereses_dict = 'INTERESES'
    #confirma_clave = 'S1,wqewqeqw'

    errores = []
    if modo =='crear' or nombre_dict in data:
        nombre = data.get(nombre_dict,'').strip()
        if not nombre:
            errores.append('El nombre es obligatiorio.')
        elif not nombre.replace(' ', '').isalpha():
            errores.append('Nombre: Solo debe contener letras.')
            
    if modo =='crear' or apellido_dict in data:
        apellido = data.get(apellido_dict,'').strip()
        if not apellido:
            errores.append('El apellido es obligatorio.')
        elif not apellido.replace(' ', '').isalpha():
            errores.append('Apellido: Solo debe contener letras.')

    if modo == 'crear' or correo_dict in data:
        correo = data.get(correo_dict,'').strip()
        if not correo:
            errores.append('El correo es obligatorio.')
        elif not correo.endswith('@duocuc.cl'):
            errores.append('El correo debe se de propiedad "@duocuc.cl".')
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append('Correo: Formato inválido.')
    
    if modo == 'crear' or id_carrera_dict in data:
        id_carrera = data.get(id_carrera_dict,'')
        if not id_carrera:
            errores.append('La carrera es obligatoria.')
        valida_id_carrera_num = id_carrera.isdigit()
        if valida_id_carrera_num == False:
            errores.append('Formato de carrera incorrecto.')


    if modo == 'crear' or intereses_dict in data:
        intereses = data.get(intereses_dict, '')
        if isinstance(intereses, str):
            intereses = intereses.strip()
            if not intereses:
                errores.append('Agregar al menos un interés es obligatorio.')
        elif isinstance(intereses, list):
            if not intereses:
                errores.append('Agregar al menos un interés es obligatorio.')
        else:
            errores.append('El campo intereses tiene un formato inválido.') 

    if modo == 'crear' or clave_dict in data:
        clave = data.get(clave_dict,'').strip()
        if not clave:
            errores.append('La contraseña es un campo obligatorio.')
        else:
            if len(clave)<8:
                errores.append('Contraseña: Debe ser mayor a 8 caracteres.')
            if data.get(correo_dict,'').strip() and data.get(correo_dict,'').split('@')[0].lower() in clave.lower():
                errores.append('Contraseña: No puede contener parte del correo.')
            if data.get(correo_dict,'').strip() and data.get(correo_dict,'').lower() in clave.lower():
                errores.append('Contraseña: No puede contener parte del nombre.')
            if not re.search(r'[A-Z]', clave):
                errores.append('Contraseña: Debe tener al menos una letra mayúscula.')
            if not re.search(r'[a-z]', clave):
                errores.append('Contraseña: Debe teber al menos una letra minúscula.')
            if not re.search(r'\d', clave):
                errores.append('Contraseña: Debe tener al menos un número.')
            if not re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]', clave):
                errores.append('Contraseña: Debe tener a lo menos 1 carácter especial.')

    return errores

    
def trae_ruta_imagen(tipo):
    return os.path.join(UPLOAD_FOLDER,'usuario', tipo)



def eliminar_imagen(tipo, nombre_archivo):
    print(nombre_archivo,"Eliminar")
    if nombre_archivo not in ['default_perfil.png', 'default_portada.png']:
        ruta = os.path.join(UPLOAD_FOLDER, 'usuario', tipo, nombre_archivo)
        if os.path.exists(ruta):
            os.remove(ruta)