
SESSION_KEY = 'usuario_sesion'


def get_usuario_sesion(request):

    return request.session.get(SESSION_KEY, None)


def get_comentarios_por_publicacion(pub_id=None, pub_titulo=None):

    try:
        from .models import Comentario
        queryset = Comentario.objects.filter(
            estado=Comentario.EstadoComentarioChoices.VISIBLE
        )

        if pub_id:
            queryset = queryset.filter(publicacion__id=pub_id)
        elif pub_titulo:
            queryset = queryset.filter(publicacion__titulo=pub_titulo)

        return list(queryset.order_by('-fecha_comentario'))
    except Exception as e:
        print(f"[ERROR] get_comentarios_por_publicacion: {e}")
        return []


def get_publicaciones_activas(limite=8):
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

    try:
        from apps.publicaciones.models import Publicacion
        return Publicacion.objects.get(pk=pub_id)
    except Exception:
        return None


def get_usuario_por_correo(correo):
    try:
        from apps.accounts.models import Usuario
        return Usuario.objects.get(correo=correo)
    except Exception:
        return None