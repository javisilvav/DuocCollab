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

def usa_api(token, metodo, endpoint, requiere_tkn=True,**kwargs):
    token = request.session.get('jwt_token') if requiere_tkn else None
    valor = verificar_token_y_api(token, metodo, endpoint, requiere_tkn,**kwargs)
    if valor == 'No existe token':
        return redirect('Login')
    if valor == 'Sesión Expirada':
        return redirect('Login')
    if valor == 'No existe token':
        return redirect('Login')
    
    return valor


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
        response = consulta_mis_proyectos(token)
        
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
        response = consulta_mis_proyectos(token)
        
        if 'error' in response:
            request.session['sweet_alert'] = alert('error', 'Error', response['error'])
            return redirect('Perfil')
        else:
            request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación creada correctamente.')
            return redirect('Perfil')



def SubirProyecto(request):
  if request.method == 'GET':
    #Obtener Etiquetas
    result_etiqueta = verificar_token_y_api(request, 'GET', '/proyecto/etiquetas', 'Perfil')
    if isinstance(result_etiqueta, HttpResponseRedirect):
        return result_etiqueta
    response_etiqueta = result_etiqueta['response']
    if response_etiqueta.status_code == 200:
        etiquetas = response_etiqueta.json()
    else:
        request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las etiquetas.')
        return redirect('Perfil')
    
    result_correo = verificar_token_y_api(request, 'GET', '/auth/correos', 'Perfil')
    if isinstance(result_correo, HttpResponseRedirect):
        return result_correo
    response_correo = result_correo['response']
    if response_correo.status_code == 200:
        correos = response_correo.json()
    else:
        request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los correos.')
        return redirect('Perfil')
    
    #Obtener carreras
    result_carrera = verificar_token_y_api(request, 'GET', '/institucion/carreras', 'Login', False)
    if isinstance(result_carrera, HttpResponseRedirect):
        return result_carrera
    response_carrera = result_carrera['response']
    if response_carrera.status_code == 200:
        carreras = response_carrera.json()
    else:
      request.session['sweet_alert'] = alert('error', 'Error', "No se pudieron obtener las carreras")
      return redirect('Login')
        

    #Obtener SEDE
    result_sede = verificar_token_y_api(request, 'GET', '/institucion/sedes', 'Login', False)
    if isinstance(result_sede, HttpResponseRedirect):
        return result_sede
    response_sede = result_sede['response']
    if response_sede.status_code == 200:
        sedes = response_sede.json()
    else:
      request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las sedes.')
      return redirect('Login')

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

        result = verificar_token_y_api(request, 'POST', '/proyecto/crear', 'Perfil', data=datos, files=archivos)
        if isinstance(result, HttpResponseRedirect):
            return result
        response = result['response']
        if response.status_code == 201:
            request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto creado y publicado correctamente.')
            return redirect('Perfil')
        else:
            try:
                
                
                request.session['sweet_alert'] = alert('error', 'Error al crear proyecto.', 'error')
                return redirect('Perfil')
            except ValueError:
                error = f"Error inesperado ({response.status_code}): {response.text}"
                request.session['sweet_alert'] = alert('error', 'Error', error)
                return redirect('Perfil')


       




def Proyectos(request):
    if request.method == 'GET':
        result = verificar_token_y_api(request, 'GET', '/proyecto/proyectos', 'Home')
        if isinstance(result, HttpResponseRedirect):
            return result
        response = result['response']
        if response.status_code == 200:
            proyecto = response.json()
            for i in proyecto:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
        else:
          request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los proyectos')
          return redirect('Home')       
        contexto = {
            'proyectos': proyecto
        }
        return render(request, 'proyectos.html', contexto)



def Admin(request):
    print(request.method)
    if request.method == 'GET':
        contexto = {
            'sweet_alert': request.session.pop('sweet_alert', None)
        }
        return render(request, 'admin/admin.html', contexto)


def Inicio(request):
    if request.method == 'GET':
        result = verificar_token_y_api(request, 'GET', '/auth/count_user', 'Admin')
        if isinstance(result, HttpResponseRedirect):
            return result
        response = result['response']
        if response.status_code == 200:
            contador = response.json()
        else:
          contador = 0

        result_project = verificar_token_y_api(request, 'GET', '/proyecto/count_project', 'Admin')
        if isinstance(result_project, HttpResponseRedirect):
            return result_project
        response_project = result_project['response']
        if response_project.status_code == 200:
            cont_proyecto = response_project.json()
        else:
          cont_proyecto = 0


        result_post_pendiente = verificar_token_y_api(request, 'GET', '/proyecto/count_postulacion_pendiente', 'Admin')
        if isinstance(result_post_pendiente, HttpResponseRedirect):
            return result_post_pendiente
        response_post_pendiente = result_post_pendiente['response']
        if response_post_pendiente.status_code == 200:
            cont_post_pendiente = response_post_pendiente.json()
        else:
          cont_post_pendiente = 0


        result_ultimos_usuarios = verificar_token_y_api(request, 'GET', '/auth/ultimos_usuarios', 'Admin')
        if isinstance(result_ultimos_usuarios, HttpResponseRedirect):
            return result_ultimos_usuarios
        response_ultimos_usuarios = result_ultimos_usuarios['response']
        if response_ultimos_usuarios.status_code == 200:
            ultimos_usuarios = response_ultimos_usuarios.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los ultimos registros de usuarios.')
            return redirect('Admin')
   
        contexto = {
            'contador': contador,
            'cont_proyecto': cont_proyecto,
            'cont_post_pendiente':cont_post_pendiente,
            'ultimos_usuarios':ultimos_usuarios
        }
        return render(request, 'admin/home.html',contexto)


def EscuelasAdmin(request):
    if request.method == 'GET':
        #Obtener ESCUELA
        result_escuela = verificar_token_y_api(request, 'GET', '/institucion/escuelas', 'Login', False)
        if isinstance(result_escuela, HttpResponseRedirect):
            return result_escuela
        response_escuela = result_escuela['response']
        if response_escuela.status_code == 200:
            escuelas = response_escuela.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las escuelas.')
            return redirect('Login')
        sweet_alert = request.session.pop('sweet_alert', None)
        contexto = {
        'escuelas':escuelas,
        'sweet_alert': sweet_alert
        }
        return render(request, 'admin/escuela.html', contexto)
    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {'nombre_escuela': request.POST.get('nombre')}

            result = verificar_token_y_api(request, 'POST', '/institucion/crear_escuela', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Escuela creada correctamente.')
                return redirect('Admin')
            else:
                try:
                    request.session['sweet_alert'] = alert('error', 'Error al crear escuela.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
        if request.POST.get('accion') == 'editar':    
            datos = {
                'id': request.POST.get('id_escuela_editar'),
                'nombre_escuela': request.POST.get('nuevo_nombre'),
            }
            print(datos)
            result = verificar_token_y_api(request, 'POST', '/institucion/editar_escuela', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de escuela editado correctamente.')
                return redirect('Admin')
            else:
                try:
                    request.session['sweet_alert'] = alert('error', 'Error al actualizar nombre de la escuela.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
       



def Carreras(request):
    if request.method == 'GET':
        #Obtener carreras
        result_carrera = verificar_token_y_api(request, 'GET', '/institucion/carreras', 'Login', False)
        if isinstance(result_carrera, HttpResponseRedirect):
            return result_carrera
        response_carrera = result_carrera['response']
        if response_carrera.status_code == 200:
            carreras = response_carrera.json()
        else:
            mensaje_error = 'No se pudieron obtener las carreras'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Login')
        
        #Obtener ESCUELA
        result_escuela = verificar_token_y_api(request, 'GET', '/institucion/escuelas', 'Login', False)
        if isinstance(result_escuela, HttpResponseRedirect):
            return result_escuela
        response_escuela = result_escuela['response']
        if response_escuela.status_code == 200:
            escuelas = response_escuela.json()
        else:
            mensaje_error = 'No se pudieron obtener las escuelas.'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Login')
        

        contexto = {
            'sweet_alert': request.session.pop('sweet_alert', None),
            'carreras':carreras,
            'escuelas':escuelas
        }
        return render(request, 'admin/carrera.html', contexto)
    
    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {
                'nombre_carrera':request.POST.get('nombre'),
                'id_escuela': request.POST.get('id_escuela')
            }

            result = verificar_token_y_api(request, 'POST', '/institucion/crear_carrera', 'Admin', json=datos, headers={'Content-Type':'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Carrera creada correctamente.')
                return redirect('Admin')
            else:
                try:
                    
                    
                    request.session['sweet_alert'] = alert('error', 'Error al crear Carrera.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_carrera_editar'),
                'nombre_carrera': request.POST.get('nuevo_nombre'),
                'id_escuela': request.POST.get('id_escuela_editar'),
            }
            print(datos)
            result = verificar_token_y_api(request, 'POST', '/institucion/editar_carrera', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de carrera editado correctamente.')
                return redirect('Admin')
            else:
                try:
                    
                    
                    request.session['sweet_alert'] = alert('error', 'Error al actualizar nombre de la carrera.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')




def Sede(request):
    if request.method == 'GET':

        #Obtener SEDE
        result_sede = verificar_token_y_api(request, 'GET', '/institucion/sedes', 'Login', False)
        if isinstance(result_sede, HttpResponseRedirect):
            return result_sede
        response_sede = result_sede['response']
        if response_sede.status_code == 200:
            sedes = response_sede.json()
        else:
          mensaje_error = 'No se pudieron obtener las sedes.'
          request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
          return redirect('Login')
        

        contexto = {
        'sweet_alert': request.session.pop('sweet_alert', None),
        'sedes':sedes
        }

        return render(request, 'admin/sede.html', contexto)
    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {'nombre_sede': request.POST.get('nombre')}

            result = verificar_token_y_api(request, 'POST', '/institucion/crear_sede', 'Admin', json=datos, headers={'Content-Type':'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Sede creada correctamente.')
                return redirect('Admin')
            else:
                try:
                    
                    
                    request.session['sweet_alert'] = alert('error', 'Error al crear sede.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
        
        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_sede_editar'),
                'nombre_sede': request.POST.get('nuevo_nombre'),
            }
            print(datos)
            result = verificar_token_y_api(request, 'POST', '/institucion/editar_sede', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de sede editado correctamente.')
                return redirect('Admin')
            else:
                try:
                    
                    
                    request.session['sweet_alert'] = alert('error', 'Error al actualizar nombre de la sede.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')



def SedeEscuela(request):
    if request.method == 'GET':
        #Obtener SEDE
        result_sede = verificar_token_y_api(request, 'GET', '/institucion/sedes', 'Login', False)
        if isinstance(result_sede, HttpResponseRedirect):
            return result_sede
        response_sede = result_sede['response']
        if response_sede.status_code == 200:
            sedes = response_sede.json()
        else:
            mensaje_error = 'No se pudieron obtener las sedes.'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Login')
    
        #Obtener ESCUELA
        result_escuela = verificar_token_y_api(request, 'GET', '/institucion/escuelas', 'Login', False)
        if isinstance(result_escuela, HttpResponseRedirect):
            return result_escuela
        response_escuela = result_escuela['response']
        if response_escuela.status_code == 200:
            escuelas = response_escuela.json()
        else:
            mensaje_error = 'No se pudieron obtener las escuelas.'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Login')
    

        #Obtener SEDE y ESCUELA
        result_sede_escuela = verificar_token_y_api(request, 'GET', '/institucion/sede_escuela', 'Login', False)
        if isinstance(result_sede_escuela, HttpResponseRedirect):
            return result_sede_escuela
        response_sede_escuela = result_sede_escuela['response']
        if response_sede_escuela.status_code == 200:
            sede_escuela = response_sede_escuela.json()
        else:
          mensaje_error = 'No se pudieron obtener las sedes y escuelas.'
          request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
          return redirect('Login')

        contexto = {
            'sweet_alert': request.session.pop('sweet_alert', None),
            'sedes': sedes,
            'sede_escuela':sede_escuela,
            'escuelas':escuelas
        }
        return render(request, 'admin/sede_escuela.html', contexto)
    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {
                "id_sede":request.POST.get('sede'),
                "id_escuela":request.POST.get('escuela')
            }

            result = verificar_token_y_api(request, 'POST', '/institucion/crear_sd_esc', 'Admin', json=datos, headers={'Content-Type':'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Sede y escuela relacionada correctamente.')
                return redirect('Admin')
            else:
                try:
                    
                    
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al relacionar sede y escuela.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
                
        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_sd_esc_editar'),
                'nueva_sede': request.POST.get('sede_nueva'),
                'nueva_escuela': request.POST.get('escuela_nueva'),
            }
            result = verificar_token_y_api(request, 'POST', '/institucion/editar_sd_esc', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Nombre de sede y escuela editado correctamente.')
                return redirect('Admin')
            else:
                try:                   
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al actualizar nombre de la sede y escuela.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')




def Usuarios(request):
    if request.method == 'GET':
        #Obtener carreras
        result_carrera = verificar_token_y_api(request, 'GET', '/institucion/carreras', 'Admin', False)
        if isinstance(result_carrera, HttpResponseRedirect):
            return result_carrera
        response_carrera = result_carrera['response']
        if response_carrera.status_code == 200:
            carreras = response_carrera.json()
        else:
            mensaje_error = 'No se pudieron obtener las carreras'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Admin')
        
        #Obtener Etiquetas
        result_etiqueta = verificar_token_y_api(request, 'GET', '/proyecto/etiquetas', 'Admin')
        if isinstance(result_etiqueta, HttpResponseRedirect):
            return result_etiqueta
        response_etiqueta = result_etiqueta['response']
        if response_etiqueta.status_code == 200:
            etiquetas = response_etiqueta.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las etiquetas.')
            return redirect('Admin')
    
            
    

        #Obtener Usuarios
        result_usuarios = verificar_token_y_api(request, 'GET', '/auth/usuarios_registrados', 'Admin')
        if isinstance(result_usuarios, HttpResponseRedirect):
            return result_usuarios
        response_usuario = result_usuarios['response']
        if response_usuario.status_code == 200:
            usuarios = response_usuario.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los registros de usuarios.')
            return redirect('Admin')

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

            try:
                result = verificar_token_y_api(request,'POST', '/auth/registro', 'Admin',requiere_tkn=False, json=datos, headers={'Content-Type': 'application/json'})
                if isinstance(result, HttpResponseRedirect):
                    return result
                
                
                response = result['response']
                if response.status_code == 201:
                    # Mensaje SweetAlert para registro exitoso
                    request.session['sweet_alert'] = alert('success', 'Registro Exitoso', 'Usuario registrado correctamente. Por favor, inicia sesión.')
                    return redirect('Login')
                else:                   
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al registrar usuario.')
                    return redirect('Admin')
            except Exception as e:
                return render(request, 'admin/usuario.html', {'error': str(e)})


        if request.POST.get('accion') == 'editar':
            result = verificar_token_y_api(request, 'GET', '/auth/usuario_actual', 'Admin')
            if isinstance(result, HttpResponseRedirect):
                return result
            usuario_actual = result['response'].json() if result['response'].status_code == 200 else {}

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
    
            result = verificar_token_y_api(request, 'PUT', '/auth/editar', 'Admin', data=datos, files=archivos)
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']

            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Usuario actualizado correctamente.')
                return redirect('Admin')
            else:
                try:               
                    request.session['sweet_alert'] = alert('error', 'Error al editar usuario.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')   




def Etiquetas(request):
    if request.method == 'GET':
        #Obtener Etiquetas
        result_etiqueta = verificar_token_y_api(request, 'GET', '/proyecto/etiquetas', 'Perfil')
        if isinstance(result_etiqueta, HttpResponseRedirect):
            return result_etiqueta
        response_etiqueta = result_etiqueta['response']
        if response_etiqueta.status_code == 200:
            etiquetas = response_etiqueta.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las etiquetas.')
            return redirect('Perfil')   
        
        contexto = {
        'etiquetas': etiquetas
        }
        return render(request, 'admin/etiqueta.html', contexto)
    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {'nombre_etiqueta': request.POST.get('etiqueta')}

            result = verificar_token_y_api(request, 'POST', '/proyecto/crear_etiqueta', 'Admin', json=datos, headers={'Content-Type':'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Etiqueta creada correctamente.')
                return redirect('Admin')
            else:
                try:  
                    request.session['sweet_alert'] = alert('error', 'Error al crear etiqueta.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
        

        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_etiqueta_editar'),
                'nueva_etiqueta': request.POST.get('nuevo_nombre'),
            }
            result = verificar_token_y_api(request, 'POST', '/proyecto/editar_etiqueta', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Etiqueta editada correctamente.')
                return redirect('Admin')
            else:
                try:                   
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al actualizar nombre de la etiqueta.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
                

            

def ProyectosAdmin(request):
    if request.method == 'GET':

        #Obtener SEDE
        result_sede = verificar_token_y_api(request, 'GET', '/institucion/sedes', 'Login', False)
        if isinstance(result_sede, HttpResponseRedirect):
            return result_sede
        response_sede = result_sede['response']
        if response_sede.status_code == 200:
            sedes = response_sede.json()
        else:
            mensaje_error = 'No se pudieron obtener las sedes.'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Login')
        
        #Obtener Usuarios
        result_usuarios = verificar_token_y_api(request, 'GET', '/auth/usuarios_registrados', 'Admin')
        if isinstance(result_usuarios, HttpResponseRedirect):
            return result_usuarios
        response_usuario = result_usuarios['response']
        if response_usuario.status_code == 200:
            usuarios = response_usuario.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los registros de usuarios.')
            return redirect('Admin')
        
        #Obtener carreras
        result_carrera = verificar_token_y_api(request, 'GET', '/institucion/carreras', 'Login', False)
        if isinstance(result_carrera, HttpResponseRedirect):
            return result_carrera
        response_carrera = result_carrera['response']
        if response_carrera.status_code == 200:
            carreras = response_carrera.json()
        else:
            mensaje_error = 'No se pudieron obtener las carreras'
            request.session['sweet_alert'] = alert('error', 'Error', mensaje_error)
            return redirect('Admin')

        #Obtener proyectos
        result_proyectos = verificar_token_y_api(request, 'GET', '/proyecto/proyectos', 'Admin')
        if isinstance(result_proyectos, HttpResponseRedirect):
            return result_proyectos
        response_proyecto = result_proyectos['response']
        if response_proyecto.status_code == 200:
            proyectos = response_proyecto.json()
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los proyectos')
            return redirect('Admin')       
                
        
        contexto = {
        
        'proyectos':proyectos,
        'carreras':carreras,
        'sedes':sedes,
        'usuarios':usuarios,
        }
        return render(request, 'admin/proyecto.html', contexto)
    if request.method == 'POST':
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

            result = verificar_token_y_api(request, 'POST', '/proyecto/crear', 'Admin', data=datos, files=archivos)
            if isinstance(result, HttpResponseRedirect):
                return result
            
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto creado y publicado correctamente.')
                return redirect('Admin')
            else:
                try:               
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al crear proyecto.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
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

            

            result = verificar_token_y_api(request, 'POST', '/proyecto/editar', 'Admin', data=datos, files=archivos)
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto editado correctamente.')
                return redirect('Admin')
            else:
                try:
                    request.session['sweet_alert'] = alert('error', 'Error al editar proyecto.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
        



def ProyectoEtiqueta(request):
    if request.method == 'GET':
        #Obtener proyectos
        result_proyectos = verificar_token_y_api(request, 'GET', '/proyecto/proyectos', 'Admin')
        if isinstance(result_proyectos, HttpResponseRedirect):
            return result_proyectos
        response_proyecto = result_proyectos['response']
        if response_proyecto.status_code == 200:
            proyectos = response_proyecto.json()
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los proyectos')
            return redirect('Admin')     

        #Obtener Etiquetas
        result_etiqueta = verificar_token_y_api(request, 'GET', '/proyecto/etiquetas', 'Admin')
        if isinstance(result_etiqueta, HttpResponseRedirect):
            return result_etiqueta
        response_etiqueta = result_etiqueta['response']
        if response_etiqueta.status_code == 200:
            etiquetas = response_etiqueta.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las etiquetas.')
            return redirect('Admin')     
        

        #Obtener proyecto_etiqueta
        result_etiqueta_proyecto = verificar_token_y_api(request, 'GET', '/proyecto/proyecto_etiqueta', 'Admin')
        if isinstance(result_etiqueta_proyecto, HttpResponseRedirect):
            return result_etiqueta_proyecto
        response_etiqueta_proyecto = result_etiqueta_proyecto['response']
        if response_etiqueta_proyecto.status_code == 200:
            proyecto_etiqueta = response_etiqueta_proyecto.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener las etiquetas.')
            return redirect('Admin')     


        contexto = {
        'proyecto_etiquetas':proyecto_etiqueta,
        'etiquetas':etiquetas,
        'proyectos':proyectos
        }
        return render(request, 'admin/proyecto_etiqueta.html', contexto)
    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {
                'proyecto': request.POST.get('proyecto'),
                'etiqueta': request.POST.get('etiqueta'),
            }

            result = verificar_token_y_api(request, 'POST', '/proyecto/crear_proyecto_etiqueta', 'Admin', json=datos, headers={'Content-Type':'application/json'})

            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Proyecto y etiqueta relacionada correctamente.')
                return redirect('Admin')
            else:
                try:
                    
                    
                    request.session['sweet_alert'] = alert('error', 'Error al relacionar etiqueta y proyecto.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')



        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_tabla_editar'),
                'nuevo_proyecto': request.POST.get('proyecto_nuevo'),
                'nueva_etiqueta': request.POST.get('etiqueta_nueva'),
            }
            result = verificar_token_y_api(request, 'POST', '/proyecto/editar_proyecto_etiqueta', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Etiqueta de proyecto editada correctamente.')
                return redirect('Admin')
            else:
                try:                   
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al actualizar etiqueta de proyecto.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')



def IntegrantesProyecto(request):
    if request.method == 'GET':
        #Obtener Usuarios
        result_usuarios = verificar_token_y_api(request, 'GET', '/auth/usuarios_registrados', 'Admin')
        if isinstance(result_usuarios, HttpResponseRedirect):
            return result_usuarios
        response_usuario = result_usuarios['response']
        if response_usuario.status_code == 200:
            usuarios = response_usuario.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los registros de usuarios.')
            return redirect('Admin')
    
        #Obtener proyectos e integtantes
        result_proyectos = verificar_token_y_api(request, 'GET', '/proyecto/proyectos_integrantes', 'Admin')
        if isinstance(result_proyectos, HttpResponseRedirect):
            return result_proyectos
        response_proyecto = result_proyectos['response']
        if response_proyecto.status_code == 200:
            proyectos = response_proyecto.json()
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
        if request.POST.get('accion') == 'crear':
            datos = {
                'usuario': request.POST.get('usuario'),
                'proyecto': request.POST.get('proyecto'),
                'rol': request.POST.get('rol'),
            }

            result = verificar_token_y_api(request, 'POST', '/proyecto/crear_proyectos_integrantes', 'Admin', json=datos, headers={'Content-Type':'application/json'})

            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Integrante y proyecto creado correctamente.')
                return redirect('Admin')
            else:
                try:
                    request.session['sweet_alert'] = alert('error', 'Error al relacionar integrante y proyecto.', 'error')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
                

        if request.POST.get('accion') == 'editar':
            datos = {
                'id': request.POST.get('id_tabla_editar'),
                'proyecto': request.POST.get('proyecto_nuevo'),
                'usuario': request.POST.get('integrante_nuevo'),
                'rol':request.POST.get('rol_nuevo'),
            }
            result = verificar_token_y_api(request, 'POST', '/proyecto/editar_proyectos_integrantes', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Integrantes de proyecto editado correctamente.')
                return redirect('Admin')
            else:
                try:                   
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al actualizar integrantes de proyecto.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')











def Postulaciones(request):  
    if request.method == 'GET':
        #Obtener Usuarios
        result_usuarios = verificar_token_y_api(request, 'GET', '/auth/usuarios_registrados', 'Admin')
        if isinstance(result_usuarios, HttpResponseRedirect):
            return result_usuarios
        response_usuario = result_usuarios['response']
        if response_usuario.status_code == 200:
            usuarios = response_usuario.json()
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los registros de usuarios.')
            return redirect('Admin')
    
        #Obtener proyectos
        result_proyectos = verificar_token_y_api(request, 'GET', '/proyecto/proyectos', 'Admin')
        if isinstance(result_proyectos, HttpResponseRedirect):
            return result_proyectos
        response_proyecto = result_proyectos['response']
        if response_proyecto.status_code == 200:
            proyectos = response_proyecto.json()
            for i in proyectos:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los proyectos')
            return redirect('Admin')    
    
        #Obtener postulaciones
        result_postulaciones = verificar_token_y_api(request, 'GET', '/proyecto/postulaciones', 'Admin')
        if isinstance(result_postulaciones, HttpResponseRedirect):
            return result_postulaciones
        response_proyecto = result_postulaciones['response']
        if response_proyecto.status_code == 200:
            postulaciones = response_proyecto.json()
            for i in postulaciones:
                filename = i.get('FOTO_PROYECTO')
                if filename:
                    filename = i['FOTO_PROYECTO'] = ruta_img_proyecto(filename)     
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los postulaciones')
            return redirect('Admin')    
    
        result = verificar_token_y_api(request,'GET', '/proyecto/postulaciones', 'Home')
        if isinstance(result, HttpResponseRedirect):
            return result
        response = result['response']
        if response.status_code == 200:
            postulacion = response.json()
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
        else:
            request.session['sweet_alert'] = alert('error', 'Error', 'No se pudieron obtener los postulaciones')
            return redirect('Admin')    

        contexto = {
        'postulaciones': postulacion,
        'proyectos':proyectos,
        'usuarios':usuarios
        }
        return render(request, 'admin/postulacion.html', contexto)


    if request.method == 'POST':
        if request.POST.get('accion') == 'crear':
            datos = {
                "ID_USUARIO": request.POST.get('usuario'),
                "ID_PROYECTO": request.POST.get('id_proyecto') , 
            }
            comentario = request.POST.get('comentario')
            if comentario:
                datos["COMENTARIO"] = 'Panel admin añadio: ' + comentario

            result = verificar_token_y_api(request, 'POST', '/proyecto/crear_postulacion_admin', 'Admin', json=datos, headers={'Content-Type': 'application/json'})
            if isinstance(result, HttpResponseRedirect):
                return result
            response = result['response']
            if response.status_code == 201:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Postulación creada correctamente.')
                return redirect('Admin')
            else:
                try:
                    request.session['sweet_alert'] = alert('error', 'Error', 'Error al crear postulación.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
                    return redirect('Admin')
        if request.POST.get('accion') == 'editar':
            datos = {
                "ID_POSTULACION":request.POST.get('id_postular_editar'),
                "ESTADO": request.POST.get('estado_nuevo')
            }
            result = verificar_token_y_api(request,'POST', '/proyecto/editar_postulacion', 'Admin', json=datos)
            if isinstance(result, HttpResponseRedirect):
                return result
            
            response = result['response']
            if response.status_code == 200:
                request.session['sweet_alert'] = alert('success', '¡Listo!', 'Error al cambiar estado de postulación.')
                return redirect('Admin')
            else:
                try:

                    request.session['sweet_alert'] = alert('error','Error', 'Error al cambiar estado de postulación.')
                    return redirect('Admin')
                except ValueError:
                    error = f"Error inesperado ({response.status_code}): {response.text}"
                    request.session['sweet_alert'] = alert('error', 'Error', error)
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
        result = verificar_token_y_api(request, 'POST', '/auth/login', 'Login',False, json=datos, headers={'Content-Type':'application/json'})
        if isinstance(result, HttpResponseRedirect):
            return result

        
        response = result['response']
        if response.status_code == 200:
            data = response.json()
            request.session['jwt_token'] = data['token']
            request.session['usuario'] = data['usuario']
            request.session['sweet_alert'] = alert('success', 'Bienvenido', 'Has iniciado sesión correctamente.')
            return redirect('Admin')
        else:
            error = response.json().get('error', 'Credenciales inválidas')
            request.session['sweet_alert'] = alert('error', 'Credenciales inválidas', error)
            return redirect('AdminLogin')
