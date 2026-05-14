"""
services.py — Capa de integración entre las 4 apps
====================================================
Este archivo es el ÚNICO punto donde interacciones
toca código de las otras apps. Si un compañero cambia
algo, solo se actualiza aquí.

CONTRATO con la app accounts (login_view debe hacer esto):
    request.session['usuario_sesion'] = {
        'id':       str(usuario.pk),
        'nombre':   usuario.nombre,
        'apellido': usuario.apellido,
        'correo':   usuario.correo,
        'carrera':  usuario.carrera,
    }
    Y en logout_view:
    request.session.flush()
"""

SESSION_KEY = 'usuario_sesion'


def get_usuario_sesion(request):
    """
    Retorna el dict del usuario logueado desde la sesión.
    Retorna None si no hay sesión activa.
    """
    return request.session.get(SESSION_KEY, None)


def set_usuario_sesion_demo(request, nombre, correo):
    """
    Solo para desarrollo. Simula lo que hace accounts en login_view.
    Eliminar o deshabilitar cuando accounts esté integrado.
    """
    request.session[SESSION_KEY] = {
        'id':       'demo-001',
        'nombre':   nombre,
        'apellido': '',
        'correo':   correo,
        'carrera':  'Demo',
    }


def get_publicaciones_activas(limite=8):
    """
    Trae las últimas publicaciones activas para mostrar en home.
    Si publicaciones no está lista, retorna lista vacía sin romper.
    """
    try:
        from apps.publicaciones.models import Publicacion
        return list(
            Publicacion.objects.filter(
                estado_publicacion=Publicacion.EstadoPublicacionChoices.ACTIVA
            )[:limite]
        )
    except Exception:
        return []


def get_publicacion(pub_id):
    """
    Trae una publicación por su ID.
    Retorna None si no existe o si publicaciones no está lista.
    """
    try:
        from apps.publicaciones.models import Publicacion
        return Publicacion.objects.get(pk=pub_id)
    except Exception:
        return None


def get_usuario_por_correo(correo):
    """
    Trae un objeto Usuario de accounts por correo.
    Útil para enriquecer datos del comentarista.
    """
    try:
        from apps.accounts.models import Usuario
        return Usuario.objects.get(correo=correo)
    except Exception:
        return None