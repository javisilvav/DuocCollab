from django.shortcuts import render, redirect
#from .api_client import iniciar_sesion, consulta_sede, consulta_carrera, consulta_escuela, registrar_usuario, trae_img_perfil, consulta_sede_escuela, consulta_etiqueta, consulta_usuario, consulta_proyecto
#from .api_client import consuta_proyecto_etiqueta, consulta_integrantes, consulta_postulacion
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
#from .decorators import login_required
from django.utils.html import strip_tags
from datetime import datetime

from .api_client import *
from django.http import HttpResponseRedirect



def format_errors(errors):
    if isinstance(errors, list):
        return '\n'.join([strip_tags(str(e)) for e in errors])
    elif isinstance(errors, dict):
        return '\n'.join([strip_tags(str(v)) for k, v in errors.items()])
    return strip_tags(str(errors))

def alert(icono, titulo, texto):
  #success
  #error
  return {
      'icon': icono,
      'title': titulo,
      'text': texto
}

def Escuelas(request):
  return render(request, 'escuelas.html')

def Home(request):
  if request.method == 'GET':
    contexto = {
        'sweet_alert': request.session.pop('sweet_alert', None)
    }
  return render(request, 'index.html', contexto)  

def Login(request):
    if request.method == 'GET':
        sweet_alert = request.session.pop('sweet_alert', None)
        contexto = {
            'sweet_alert': sweet_alert
        }
        return render(request, 'login.html', contexto)
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasena')
        datos = {'correo':correo,'clave':contrasenia}
        
        response = realiza_login(datos)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Login')
        else:
            request.session['jwt_token'] = response['token']
            request.session['usuario'] = response['usuario']
            request.session['sweet_alert'] = alert('success', 'Bienvenido', 'Has iniciado sesión correctamente.')
            return redirect('Home')

    


def Logout(request):
    request.session.flush()
    return redirect('Login')


def ResetPassword(request):
  if request.method == 'GET':
    sweet_alert = request.session.pop('sweet_alert', None)
    contexto = {
        'sweet_alert': sweet_alert
    }
    return render(request, 'reset_password.html', contexto)
  if request.method == 'POST':
    correo = request.POST.get('correo')
    datos = {'correo': correo}
    response = realiza_recuperar_credenciales(datos)
    if 'error' in response:
        request.session['sweet_alert'] = alert('error', 'Error', response['error'])
        return redirect('ResetPassword')
    else:
        request.session['sweet_alert'] = alert('success', '¡Revisa tu correo!', response['mensaje'])
        return redirect('Login')

    

def Signup(request):
    if request.method == 'GET':
        

        response_sede = consulta_sede()
        if 'error' in response_sede:
            request.session['sweet_alert'] = alert('error', 'Error', response_sede['error'])
            return redirect('Login')
        else:
            sedes = response_sede

        response_carrera = consulta_carrera()
        if 'error' in response_carrera:
            request.session['sweet_alert'] = alert('error', 'Error', response_carrera['error'])
            return redirect('Login')
        else:
            carreras = response_carrera

        response_escuela = consulta_escuela()
        if 'error' in response_escuela:
            request.session['sweet_alert'] = alert('error', 'Error', response_escuela['error'])
            return redirect('Login')
        else:
            escuelas = response_escuela

        sweet_alert = request.session.pop('sweet_alert', None)
        contexto = {
          'sweet_alert': sweet_alert,
          'sedes':sedes,
          'carreras':carreras,
          'escuelas':escuelas
        }
        return render(request, 'signup.html', contexto)
    

    if request.method == 'POST':
        datos = {
            "NOMBRE": request.POST.get('nombre'),
            "APELLIDO": request.POST.get('apellido'),
            "CORREO": request.POST.get('correo'),
            "CONTRASENIA": request.POST.get('contrasena'),
            "ID_CARRERA": request.POST.get('carrera'),
            "ID_SEDE": request.POST.get('sede'),
            "INTERESES": request.POST.get('intereses'),
            "FOTO_PERFIL": None,
            "FOTO_PORTADA": None
        }

        try:
            response = realiza_nueva_cuenta(datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error',  response['error'])
                return redirect('Signup')
            else:
                request.session['sweet_alert'] = alert('success', 'Registro Exitoso', response['mensaje'])
                return redirect('Login')
        except Exception as e:
            return render(request, 'signup.html', alert('success', 'Error', str(e)))

    
    

def Perfil(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_usuario_actual(token)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Login')
        else:
 
            url_perfil, url_portada = ruta_img_perfil_portada(response['FOTO_PERFIL'], response['FOTO_PORTADA'])
            sweet_alert = request.session.pop('sweet_alert', None)
            context = {
                'usuario': response,
                'foto_perfil':url_perfil,
                'foto_portada':url_portada
            }
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'perfil.html', context)



        


def EditarPerfil(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_usuario_actual(token)
        
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Perfil')
        else:
            sweet_alert = request.session.pop('sweet_alert', None)
            context = {'usuario': response}
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'editar_perfil.html', context)

    elif request.method == 'POST':
        token = request.session.get('jwt_token')
        response = consulta_usuario_actual(token)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Perfil')
        else:
            usuario_actual = response
            datos = {}
            campos = {
                'NOMBRE': 'nombre',
                'APELLIDO': 'apellido',
                'CONTRASENIA': 'contrasena',
                'CORREO': 'correo',
                'INTERESES': 'intereses',
            }

            for key_api, key_form in campos.items():
                valor = request.POST.get(key_form, '').strip()
                if valor:  # Solo enviar si el campo tiene un valor no vacío
                    # Opción: no enviar si no ha cambiado
                    if key_api in usuario_actual:
                        if str(usuario_actual[key_api]).strip() == valor:
                            continue  # no lo mandamos si no cambió
                    datos[key_api] = valor

            archivos = {}
            if 'foto_perfil' in request.FILES:
                f = request.FILES['foto_perfil']
                archivos['FOTO_PERFIL'] = (f.name, f.file, f.content_type)
            if 'foto_portada' in request.FILES:
                f = request.FILES['foto_portada']
                archivos['FOTO_PORTADA'] = (f.name, f.file, f.content_type)

            
            response = realiza_editar_perfil(token,datos,archivos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Perfil')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', response['mensaje'])
                return redirect('Perfil')


def MisProyectos(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_mis_proyectos(token)
        
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Login')
        elif 'mensaje' in response:
            sweet_alert = request.session.pop('sweet_alert', None)
            context = {
                'proyectos': [],
                'etiquetas':[]
            }
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'misproyectos.html', context)
        else:
            proyecto = response
            for i in proyecto:
                # Formatear FECHA_INICIO
                fecha = i.get('FECHA_INICIO')
                if fecha:
                    fecha_formateada = datetime.fromisoformat(fecha)
                    i['FECHA_INICIO'] = fecha_formateada.strftime("%d/%m/%Y")
                # Formatear FECHA_POSTULACION dentro de POSTULACION[]
                postulaciones = i.get('POSTULACION', [])
                for postulacion in postulaciones:
                    fecha_postulacion = postulacion.get('FECHA_POSTULACION')
                    if fecha_postulacion:
                        try:
                            fecha_formateada = datetime.strptime(fecha_postulacion, "%Y-%m-%dT%H:%M:%S.%f")
                        except ValueError:
                        # En caso de que no tenga microsegundos, prueba sin ellos
                            fecha_formateada = datetime.strptime(fecha_postulacion, "%Y-%m-%dT%H:%M:%S")
                        postulacion['FECHA_POSTULACION'] = fecha_formateada.strftime("%d/%m/%Y")
                # Imagen
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)  

            response_etiqueta = consulta_etiquetas(token)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Perfil')
            else:
                etiquetas = response_etiqueta
            sweet_alert = request.session.pop('sweet_alert', None)
            context = {
                'proyectos': proyecto,
                'etiquetas':etiquetas
            }
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'misproyectos.html', context)

    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'aceptar':
            id_postulacion = request.POST.get('id_postulacion')
            datos = {
                "ID_POSTULACION":id_postulacion,
                "ESTADO":"Aceptada"
            }
            response = realiza_editar_postulacion(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Perfil')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación aceptada.')
                return redirect('Perfil')
  
        if request.POST.get('accion') == 'rechazar':
            id_postulacion = request.POST.get('id_postulacion')
            datos = {
                "ID_POSTULACION":id_postulacion,
                "ESTADO":"Rechazada"
            }
            response = realiza_editar_postulacion(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Perfil')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación rechazada.')
                return redirect('Perfil')
        
        if request.POST.get('accion') == 'editar_proyecto':
            estado = None
            if request.POST.get('estado_proyecto') == 'on':
                estado = 'TRUE'
            else:
                estado = 'FALSE'
            datos = {
                "ID_PROYECTO": request.POST.get('id_proyecto'),
                'TITULO': request.POST.get('titulo'),
                'NOMBRE_PROYECTO': request.POST.get('nombre_proyecto'),
                'DESCRIPCION': request.POST.get('descripcion'),
                'DURACION': request.POST.get('duracion'),
                'ID_SEDE': request.POST.get('sede'),
                'REQUISITOS':request.POST.get('requisitos'),
                'CARRERA_DESTINO':request.POST.get('carrera'),
                'ESTADO': estado,
                #'INTERESES':request.POST.getlist('intereses[]'),
                #'COLABORADOR':request.POST.getlist('colaboradores[]')
            }
            archivos = {}
            if 'foto_proyecto' in request.FILES:
                f = request.FILES['foto_proyecto']
                archivos['FOTO_PROYECTO'] = (f.name, f.file, f.content_type)

            response = realiza_editar_proyecto(token, datos, archivos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Perfil')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto editado correctamente.')
                return redirect('Perfil')
        



def MisPostulaciones(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_mis_postulaciones(token)
        if 'error' in response:

            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            context = {}
            sweet_alert = request.session.pop('sweet_alert', None)
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'mispostulaciones.html', context)   
        else:
            postulacion = response
            for i in postulacion:
                fecha = i.get('FECHA_POSTULACION')
                if fecha:
                    try:
                        fecha_formateada = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError:
                    # En caso de que no tenga microsegundos, prueba sin ellos
                        fecha_formateada = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S")
                i['FECHA_POSTULACION'] = fecha_formateada.strftime("%d/%m/%Y")
                proyecto = i.get('PROYECTO',{})
                filename = proyecto.get('FOTO_PROYECTO')
                if filename:
                    filename = proyecto['FOTO_PROYECTO'] = ruta_img_proyecto(filename)      
            sweet_alert = request.session.pop('sweet_alert', None)
            context = {
                'postulaciones': postulacion
            }
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'mispostulaciones.html', context)

    if request.method == 'POST':
        token = request.session.get('jwt_token')
        

        if request.POST.get('accion') == 'cancelar':
            id_postulacion = request.POST.get('id_postulacion')
            datos = {
                "ID_POSTULACION":id_postulacion,
                "ESTADO":"Cancelada"
            }
            
            response = realiza_editar_postulacion(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Login')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación cancelada.')
                return redirect('Perfil')



def ProyectosDetail(request):
    if request.method == 'GET':
        # Si llega el parámetro por GET, lo guardas en sesión y rediriges
        id_proyecto = request.GET.get('id_proyecto')
        if id_proyecto:
            request.session['id_proyecto'] = id_proyecto
            return redirect('ProyectosDetail')  # Redirige sin el parámetro en la URL
        # Si ya tienes el id_proyecto en sesión, lo usas
        id_proyecto = request.session.pop('id_proyecto', None)
        if not id_proyecto:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se logro obtener detalles del proyecto.')
            return redirect('Proyectos')
            
        datos = {
            "id_proyecto": id_proyecto
        }
        token = request.session.get('jwt_token')
        response = consulta_detalle_proyecto(token, datos)
        
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Login')
        else:
            detalle_proyecto = response
            for i in detalle_proyecto:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)   

            proyecto = detalle_proyecto[0]

            # Construir la lista de integrantes
            integrantes = []
            for integrante in proyecto.get('INTEGRANTES_PROYECTO', []):
                usuario = integrante.get('USUARIO', {})
                nombre = usuario.get('NOMBRE', '')
                apellido = usuario.get('APELLIDO', '')
                nombre_completo = f"{nombre} {apellido}".strip()
                rol = integrante.get('ROL', '')
                integrantes.append({
                    "nombre_completo": nombre_completo,
                    "rol": rol
                })

            sweet_alert = request.session.pop('sweet_alert', None)
            context = {
                'detalle_proyectos': proyecto,
                'integrantes': integrantes
            }
            if sweet_alert:
                context['sweet_alert'] = sweet_alert
            return render(request, 'proyectos_detail.html', context)
      
    if request.method == 'POST':
        id_proyecto = request.POST.get('id_proyecto') 
        datos = {"ID_PROYECTO": id_proyecto}
        comentario = request.POST.get('comentario')
        if comentario:
            datos["COMENTARIO"] = comentario


        token = request.session.get('jwt_token')
        response = realiza_crear_postulacion(token, datos)
        
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Perfil')
        else:
            request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación creada correctamente.')
            return redirect('Perfil')



def SubirProyecto(request):
  if request.method == 'GET':

    token = request.session.get('jwt_token')
    response = consulta_etiquetas(token)
    if 'error' in response:
        request.session['sweet_alert'] = alert('error', 'Error', response['error'])
        return redirect('Perfil')
    else:
        etiquetas = response


    response_correo = consulta_correos(token)
    if 'error' in response_correo:
        request.session['sweet_alert'] = alert('error', 'Error', response_correo['error'])
        return redirect('Perfil')
    else:
        correos = response_correo

    response_carrera = consulta_carrera()
    if 'error' in response_carrera:
        request.session['sweet_alert'] = alert('error', 'Error', response_carrera['error'])
        return redirect('Perfil')
    else:
        carreras = response_carrera

    response_sede = consulta_sede()
    if 'error' in response_sede:
        request.session['sweet_alert'] = alert('error', 'Error', response_sede['error'])
        return redirect('Perfil')
    else:
        sedes = response_sede
        
    context = {
        "etiquetas":etiquetas,
        "correos":correos,
        "sedes":sedes,
        "carreras":carreras,
    }
    return render(request, 'subir_proyecto.html', context)
  

  if request.method ==  'POST':

        datos = {
            'TITULO': request.POST.get('titulo'),
            'NOMBRE_PROYECTO': request.POST.get('nombre_proyecto'),
            'DESCRIPCION': request.POST.get('descripcion'),
            'DURACION': request.POST.get('duracion'),
            'ID_SEDE': request.POST.get('sede'),
            'REQUISITOS':request.POST.get('requisitos'),
            'CARRERA_DESTINO':request.POST.get('carrera'),
            'INTERESES':request.POST.getlist('intereses[]'),
            'COLABORADOR':request.POST.getlist('colaboradores[]')
        }
        archivos = {}
        if 'foto_proyecto' in request.FILES:
            f = request.FILES['foto_proyecto']
            archivos['FOTO_PROYECTO'] = (f.name, f.file, f.content_type)

        token = request.session.get('jwt_token')
        response = realiza_crear_proyecto(token, datos, archivos)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Perfil')
        else:
            request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto creado y publicado correctamente.')
            return redirect('Perfil')


def Proyectos(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_proyectos(token)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Perfil')
        else:
            proyecto = response
            for i in proyecto:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
            contexto = {
                'proyectos': proyecto
            }
            return render(request, 'proyectos.html', contexto)


def Admin(request):
    if request.method == 'GET':
        contexto = {
            'sweet_alert': request.session.pop('sweet_alert', None)
        }
        return render(request, 'admin/admin.html', contexto)


def Inicio(request):
    if request.method == 'GET':

        token = request.session.get('jwt_token')
        response = consulta_contador_usuarios(token)
        if 'error' in response:
            contador = 0
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                       
        else:
            contador = response






        response_contador_proyecto = consulta_contador_proyectos(token)
        if 'error' in response_contador_proyecto:
            cont_proyecto = 0
            request.session['sweet_alert'] = alert('error', 'Error', response_contador_proyecto['error'])
            return redirect('Admin')
        else:
            cont_proyecto = response_contador_proyecto

        response_contador_postulacion = consulta_contador_postulacion(token)
        if 'error' in response_contador_postulacion:
            cont_post_pendiente = 0
            request.session['sweet_alert'] = alert('error', 'Error', response_contador_postulacion['error'])
            return redirect('Admin')
        else:
            cont_post_pendiente = response_contador_postulacion

        response_ultimos_usuarios = consulta_ultimos_usuarios(token)
        if 'error' in response_ultimos_usuarios:
            request.session['sweet_alert'] = alert('error', 'Error', response_ultimos_usuarios['error'])
            return redirect('Admin')
        else:
            ultimos_usuarios = response_ultimos_usuarios
        
        contexto = {
            'contador': contador,
            'cont_proyecto': cont_proyecto,
            'cont_post_pendiente':cont_post_pendiente,
            'ultimos_usuarios':ultimos_usuarios
        }
        return render(request, 'admin/home.html',contexto)


def EscuelasAdmin(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_escuela()
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            escuelas = response
        sweet_alert = request.session.pop('sweet_alert', None)
        contexto = {
        'escuelas':escuelas,
        'sweet_alert': sweet_alert
        }
        return render(request, 'admin/escuela.html', contexto)
    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {'nombre_escuela': request.POST.get('nombre')}

            response = realiza_crear_escuela(token,datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Escuela creada correctamente.')
                return redirect('Admin')
        if request.POST.get('accion') == 'editar':    
            datos = {
                'id': request.POST.get('id_escuela_editar'),
                'nombre_escuela': request.POST.get('nuevo_nombre'),
            }
            response = realiza_editar_escuela(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de escuela editado correctamente.')
                return redirect('Admin')



def Carreras(request):
    if request.method == 'GET':

        token = request.session.get('jwt_token')
        response = consulta_carrera()
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            carreras = response

        response_escuela = consulta_escuela()
        if 'error' in response_escuela:
            request.session['sweet_alert'] = alert('error', 'Error', response_escuela['error'])
            return redirect('Admin')
        else:
            escuelas = response_escuela       

        contexto = {
            'sweet_alert': request.session.pop('sweet_alert', None),
            'carreras':carreras,
            'escuelas':escuelas
        }
        return render(request, 'admin/carrera.html', contexto)
    
    if request.method == 'POST':

        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {
                'nombre_carrera':request.POST.get('nombre'),
                'id_escuela': request.POST.get('id_escuela')
            }

            response = realiza_crear_carrera(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Carrera creada correctamente.')
                return redirect('Admin')
        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_carrera_editar'),
                'nombre_carrera': request.POST.get('nuevo_nombre'),
                'id_escuela': request.POST.get('nueva_escuela'),
            }
            response = realiza_editar_carrera(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de carrera editado correctamente.')
                return redirect('Admin')



def Sede(request):
    if request.method == 'GET':
        response = consulta_sede()
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            sedes = response       

        contexto = {
        'sweet_alert': request.session.pop('sweet_alert', None),
        'sedes':sedes
        }
        return render(request, 'admin/sede.html', contexto)
    if request.method == 'POST':
        
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            print('entro')
            datos = {'nombre_sede': request.POST.get('nombre')}

            
            response = realiza_crear_sede(token, datos)
            print('nombre ',response)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Sede creada correctamente.')
                return redirect('Admin')
        
        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_sede_editar'),
                'nombre_sede': request.POST.get('nuevo_nombre'),
            }
            response = realiza_editar_sede(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de sede editado correctamente.')
                return redirect('Admin')


def SedeEscuela(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response_sede = consulta_sede()
        if 'error' in response_sede:
            request.session['sweet_alert'] = alert('error', 'Error', response_sede['error'])
            return redirect('Admin')
        else:
            sedes = response_sede

        response_escuela = consulta_escuela()
        if 'error' in response_escuela:
            request.session['sweet_alert'] = alert('error', 'Error', response_escuela['error'])
            return redirect('Admin')
        else:
            escuelas = response_escuela

        response_sede_escuela = consulta_sede_escuela(token)
        if 'error' in response_sede_escuela:
            request.session['sweet_alert'] = alert('error', 'Error', response_sede_escuela['error'])
            return redirect('Admin')
        else:
            sede_escuela = response_sede_escuela

        contexto = {
            'sweet_alert': request.session.pop('sweet_alert', None),
            'sedes': sedes,
            'sede_escuela':sede_escuela,
            'escuelas':escuelas
        }
        return render(request, 'admin/sede_escuela.html', contexto)
    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {
                "id_sede":request.POST.get('sede'),
                "id_escuela":request.POST.get('escuela')
            }
            response_crear_sede_escuela = realiza_crear_sede_escuela(token, datos)
            if 'error' in response_crear_sede_escuela:
                request.session['sweet_alert'] = alert('error', 'Error', response_crear_sede_escuela['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Sede y escuela relacionada correctamente.')
                return redirect('Admin')
                
        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_sd_esc_editar'),
                'nueva_sede': request.POST.get('sede_nueva'),
                'nueva_escuela': request.POST.get('escuela_nueva'),
            }

            response_sede_escuela = realiza_editar_sede_escuela(token, datos)
            if 'error' in response_sede_escuela:
                request.session['sweet_alert'] = alert('error', 'Error', response_sede_escuela['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de sede y escuela editado correctamente.')
                return redirect('Admin')
            



def Usuarios(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_carrera()
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            carreras = response

        response_etiqueta = consulta_etiquetas(token)
        if 'error' in response_etiqueta:
            request.session['sweet_alert'] = alert('error', 'Error', response_etiqueta['error'])
            return redirect('Admin')
        else:
            etiquetas = response_etiqueta

        response_usuarios_registrados = consulta_usuarios_registrados(token)
        if 'error' in response_usuarios_registrados:
            request.session['sweet_alert'] = alert('error', 'Error', response_usuarios_registrados['error'])
            return redirect('Admin')
        else:
            usuarios = response_usuarios_registrados
        
        contexto = {
        'usuarios': usuarios,
        'carreras': carreras,
        'etiquetas': etiquetas,
        }
        return render(request, 'admin/usuario.html', contexto)

    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {
                "NOMBRE": request.POST.get('nombre'),
                "APELLIDO": request.POST.get('apellido'),
                "CORREO": request.POST.get('email'),
                "CONTRASENIA": request.POST.get('password'),
                "ID_CARRERA": request.POST.get('carrera'),
                "INTERESES": request.POST.get('intereses'),
                "FOTO_PERFIL": None,
                "FOTO_PORTADA": None
            }

            token = request.session.get('jwt_token')
            response_sede = realiza_nueva_cuenta(token, datos)
            if 'error' in response_sede:
                request.session['sweet_alert'] = alert('error', 'Error', response_sede['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', 'Registro Exitoso', 'Usuario registrado correctamente. Por favor, inicia sesión.')
                return redirect('Login')
              
        if request.POST.get('accion') == 'editar':
            token = request.session.get('jwt_token')
            response = consulta_usuario_actual(token)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Perfil')
            else:
                usuario_actual = response
            datos = {}
            campos = {
                'NOMBRE': 'nombre_nuevo',
                'APELLIDO': 'apellido_nuevo',
                'CONTRASENIA': 'contrasena_nueva',
                'CORREO': 'correo_nuevo',
                'INTERESES': 'intereses_nuevo',
            }

            for key_api, key_form in campos.items():
                valor = request.POST.get(key_form, '').strip()
                if valor:  # Solo enviar si el campo tiene un valor no vacío
                    # Opción: no enviar si no ha cambiado
                    if key_api in usuario_actual:
                        if str(usuario_actual[key_api]).strip() == valor:
                            continue  # no lo mandamos si no cambió
                    datos[key_api] = valor

            archivos = {}

            response_usuario = realiza_editar_perfil(token,datos,archivos)
            if 'error' in response_usuario:
                request.session['sweet_alert'] = alert('error', 'Error', response_usuario['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', response_usuario['mensaje'])
                return redirect('Admin')





def Etiquetas(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_etiquetas(token)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            etiquetas = response
       
        contexto = {
        'etiquetas': etiquetas
        }
        return render(request, 'admin/etiqueta.html', contexto)
    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {'nombre_etiqueta': request.POST.get('etiqueta')}

            response = realiza_crear_etiqueta(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Etiqueta creada correctamente.')
                return redirect('Admin')
        

        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_etiqueta_editar'),
                'nueva_etiqueta': request.POST.get('nuevo_nombre'),
            }

            response = realiza_editar_etiqueta(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Etiqueta editada correctamente.')
                return redirect('Admin')
            

def ProyectosAdmin(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_sede()
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            sedes = response

        response_usuario = consulta_usuarios_registrados(token)
        if 'error' in response_usuario:
            request.session['sweet_alert'] = alert('error', 'Error', response_usuario['error'])
            return redirect('Admin')
        else:
            usuarios = response_usuario

        response_carrera = consulta_carrera()
        if 'error' in response_carrera:
            request.session['sweet_alert'] = alert('error', 'Error', response_carrera['error'])
            return redirect('Admin')
        else:
            carreras = response_carrera

        response_proyecto = consulta_proyectos(token)
        if 'error' in response_proyecto:
            request.session['sweet_alert'] = alert('error', 'Error', response_proyecto['error'])
            return redirect('Admin')
        else:
            proyectos = response_proyecto
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     

        contexto = {
        'proyectos':proyectos,
        'carreras':carreras,
        'sedes':sedes,
        'usuarios':usuarios,
        }
        return render(request, 'admin/proyecto.html', contexto)
    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {
                'TITULO': request.POST.get('titulo'),
                'NOMBRE_PROYECTO': request.POST.get('nombre'),
                'DESCRIPCION': request.POST.get('descripcion'),
                'DURACION': request.POST.get('duracion'),
                'ID_SEDE': request.POST.get('sede'),
                'REQUISITOS':request.POST.get('requisitos'),
                'CARRERA_DESTINO':request.POST.get('carrera'),
                'INTERESES':request.POST.getlist('intereses[]'),
                'COLABORADOR':request.POST.getlist('colaboradores[]')
            }

            archivos = {}
            if 'foto_proyecto' in request.FILES:
                f = request.FILES['foto_proyecto']
                archivos['FOTO_PROYECTO'] = (f.name, f.file, f.content_type)

            response = realiza_crear_proyecto(token, datos, archivos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto creado y publicado correctamente.')
                return redirect('Admin')
 
        if request.POST.get('accion') == 'editar':
            estado = None

            if request.POST.get('estado_proyecto') == 'on':
                estado = 'TRUE'
            else:
                estado = 'FALSE'

            datos = {
                "ID_PROYECTO": request.POST.get('id_proyecto_editar'),
                'TITULO': request.POST.get('titulo_nuevo'),
                'NOMBRE_PROYECTO': request.POST.get('nombre_nuevo'),
                'DESCRIPCION': request.POST.get('descripcion_nuevo'),
                'DURACION': request.POST.get('duracion_nuevo'),
                'ID_SEDE': request.POST.get('sede_nuevo'),
                'REQUISITOS':request.POST.get('requisitos_nuevo'),
                'CARRERA_DESTINO':request.POST.get('carrera_nuevo'),
                #'INTERESES':request.POST.getlist('intereses[]'),
                #'COLABORADOR':request.POST.getlist('colaboradores[]'),
                'ESTADO': estado
            }
            archivos = {}
            if 'foto_proyecto_nuevo' in request.FILES:
                f = request.FILES['foto_proyecto_nuevo']
                archivos['FOTO_PROYECTO'] = (f.name, f.file, f.content_type)

            response = realiza_editar_proyecto(token, datos, archivos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto editado correctamente.')
                return redirect('Admin')



def ProyectoEtiqueta(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_proyectos(token)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            proyectos = response
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     

        response_etiqueta = consulta_etiquetas(token)
        if 'error' in response_etiqueta:
            request.session['sweet_alert'] = alert('error', 'Error', response_etiqueta['error'])
            return redirect('Admin')
        else:
            etiquetas = response_etiqueta

        response_etiqueta_proyecto = consulta_etiqueta_proyecto(token)
        if 'error' in response_etiqueta_proyecto:
            request.session['sweet_alert'] = alert('error', 'Error', response_etiqueta_proyecto['error'])
            return redirect('Admin')
        else:
            proyecto_etiqueta = response_etiqueta_proyecto
      

        contexto = {
        'proyecto_etiquetas':proyecto_etiqueta,
        'etiquetas':etiquetas,
        'proyectos':proyectos
        }
        return render(request, 'admin/proyecto_etiqueta.html', contexto)
    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {
                'proyecto': request.POST.get('proyecto'),
                'etiqueta': request.POST.get('etiqueta'),
            }
            
            response = realiza_crear_etiqueta_proyecto(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto y etiqueta relacionada correctamente.')
                return redirect('Admin')


        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_tabla_editar'),
                'nuevo_proyecto': request.POST.get('proyecto_nuevo'),
                'nueva_etiqueta': request.POST.get('etiqueta_nueva'),
            }

            response = realiza_editar_etiqueta_proyecto(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Etiqueta de proyecto editada correctamente.')
                return redirect('Admin')


def IntegrantesProyecto(request):
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response = consulta_usuarios_registrados(token)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Admin')
        else:
            usuarios = response


        response_proyecto_integrante = consulta_proyectos_integrante(token)
        if 'error' in response_proyecto_integrante:
            request.session['sweet_alert'] = alert('error', 'Error', response_proyecto_integrante['error'])
            return redirect('Admin')
        else:
            proyectos = response_proyecto_integrante
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)   

        contexto = {
        'proyectos':proyectos,
        'usuarios': usuarios
        }
        return render(request, 'admin/integrantes_proyecto.html', contexto)

    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {
                'usuario': request.POST.get('usuario'),
                'proyecto': request.POST.get('proyecto'),
                'rol': request.POST.get('rol')
            }
            response = realiza_crear_proyecto_integrante(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Integrante y proyecto creado correctamente.')
                return redirect('Admin')

        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_tabla_editar'),
                'proyecto': request.POST.get('proyecto_nuevo'),
                'usuario': request.POST.get('integrante_nuevo'),
                'rol':request.POST.get('rol_nuevo')
            }
            response = realiza_editar_proyecto_integrante(token, datos)
            if 'error' in response:
                request.session['sweet_alert'] = alert('error', 'Error', response['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Integrantes de proyecto editado correctamente.')
                return redirect('Admin')
         

def Postulaciones(request):  
    if request.method == 'GET':
        token = request.session.get('jwt_token')
        response_usuario = consulta_usuarios_registrados(token)
        if 'error' in response_usuario:
            request.session['sweet_alert'] = alert('error', 'Error', response_usuario['error'])
            return redirect('Admin')
        else:
            usuarios = response_usuario


        response_proyecto = consulta_proyectos(token)
        if 'error' in response_proyecto:
            request.session['sweet_alert'] = alert('error', 'Error', response_proyecto['error'])
            return redirect('Admin')
        else:
            proyectos = response_proyecto
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
        

        response_postulacion = consulta_postulacion(token)
        if 'error' in response_postulacion:
            request.session['sweet_alert'] = alert('error', 'Error', response_postulacion['error'])
            return redirect('Admin')
        else:
            postulacion = response_postulacion
            for i in postulacion:
                fecha = i.get('FECHA_POSTULACION')
                if fecha:
                    try:
                        fecha_formateada = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError:
                    # En caso de que no tenga microsegundos, prueba sin ellos
                        fecha_formateada = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S")
                i['FECHA_POSTULACION'] = fecha_formateada.strftime("%d/%m/%Y")
                proyecto = i.get('PROYECTO',{})
                filename = proyecto.get('FOTO_PROYECTO')
                if filename:
                    filename = proyecto['FOTO_PROYECTO'] = ruta_img_proyecto(filename)

        contexto = {
        'postulaciones': postulacion,
        'proyectos':proyectos,
        'usuarios':usuarios
        }
        return render(request, 'admin/postulacion.html', contexto)


    if request.method == 'POST':
        token = request.session.get('jwt_token')
        if request.POST.get('accion') == 'crear':
            datos = {
                "ID_USUARIO": request.POST.get('usuario'),
                "ID_PROYECTO": request.POST.get('id_proyecto') , 
            }
            comentario = request.POST.get('comentario')
            if comentario:
                datos["COMENTARIO"] = 'Panel admin añadio: ' + comentario
            
            response_postulacion = realiza_crear_postulacion(token, datos)
            if 'error' in response_postulacion:
                request.session['sweet_alert'] = alert('error', 'Error', response_postulacion['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación creada correctamente.')
                return redirect('Admin')
           
        if request.POST.get('accion') == 'editar':
            datos = {
                "ID_POSTULACION":request.POST.get('id_postular_editar'),
                "ESTADO": request.POST.get('estado_nuevo')
            }
            response_postulacion = realiza_editar_postulacion(token, datos)
            if 'error' in response_postulacion:
                request.session['sweet_alert'] = alert('error', 'Error', response_postulacion['error'])
                return redirect('Admin')
            else:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Cambio del estado de postulación, realizado correctamente.')
                return redirect('Admin')


def AdminLogin(request):
    if request.method == 'GET':
        sweet_alert = request.session.pop('sweet_alert', None)
        contexto = {
            'sweet_alert': sweet_alert
        }
        return render(request, 'admin/signin.html', contexto)
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('contrasena')
        datos = {'correo':correo,'clave':contrasenia}

        response = realiza_login(datos)
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('AdminLogin')
        else:
            request.session['jwt_token'] = response['token']
            request.session['usuario'] = response['usuario']
            request.session['sweet_alert'] = alert('success', 'Bienvenido', 'Has iniciado sesión correctamente.')
            return redirect('Admin')