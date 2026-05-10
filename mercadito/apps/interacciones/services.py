"""
services.py — Capa de servicios de la app 'interacciones'
==========================================================
Este archivo centraliza toda la comunicación con otras apps del proyecto.
La idea es que NUNCA importemos modelos o vistas de otras apps directamente;
en cambio, llamamos funciones de esta capa. Cuando tus compañeros suban sus
apps al repositorio, solo hay que actualizar estas funciones aquí.

Contratos esperados con otras apps:
------------------------------------
App 'usuarios':
  - Debe guardar en la sesión de Django un diccionario bajo la clave 'usuario_sesion':
        request.session['usuario_sesion'] = {
            'nombre': 'Bryan Salas',
            'correo': 'bryan@universidad.edu',
        }
  - Eso es todo lo que necesitamos de ellos.

App 'publicaciones':
  - Cuando un usuario visita una publicación, el template de esa app
    debe incluir nuestros parciales pasando los datos de la publicación
    como variables de contexto: pub_titulo, pub_categoria.
  - También puede llamar directamente a get_publicacion_resumen(pub_id)
    si en algún momento necesitamos consultar esos datos en el backend.
"""

# ---------------------------------------------------------------------------
# Constante de clave de sesión. Si el equipo de 'usuarios' decide cambiarla,
# solo se modifica aquí.
# ---------------------------------------------------------------------------
SESSION_KEY_USUARIO = 'usuario_sesion'


def get_usuario_sesion(request):
    """
    Devuelve el dict del usuario actualmente logueado desde la sesión de Django.
    Retorna None si no hay sesión activa (usuario no autenticado).

    La app 'usuarios' es responsable de escribir y limpiar esta clave de sesión
    cuando hace login / logout.

    Uso:
        usuario = get_usuario_sesion(request)
        if not usuario:
            return redirect('usuarios:login')
    """
    return request.session.get(SESSION_KEY_USUARIO, None)


def set_usuario_sesion_demo(request, nombre, correo):
    """
    Función de DEMO para simular un login mientras la app 'usuarios'
    no está disponible. Solo debe usarse en desarrollo/pruebas.

    La app 'usuarios' hará esto en su propia vista de login:
        request.session['usuario_sesion'] = {'nombre': ..., 'correo': ...}
    """
    request.session[SESSION_KEY_USUARIO] = {
        'nombre': nombre,
        'correo': correo,
    }


def get_publicacion_resumen(pub_id):
    """
    Devuelve un resumen básico de una publicación dado su ID.

    Cuando la app 'publicaciones' esté lista, importa su método aquí:
        from publicaciones.services import obtener_publicacion_por_id
        return obtener_publicacion_por_id(pub_id)

    Por ahora devuelve un dict vacío como placeholder seguro.
    """
    # TODO: reemplazar con la llamada real cuando publicaciones esté disponible
    # from publicaciones.services import obtener_publicacion_por_id
    # return obtener_publicacion_por_id(pub_id)
    return {}
