from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Favorito, Comentario
from .forms import ComentarioForm
from . import services


# ---------------------------------------------------------------------------
# VISTAS DE FAVORITOS
# ---------------------------------------------------------------------------

def guardar_favorito(request):
    """
    Guarda una publicación como favorita del usuario en sesión.
    Solo acepta POST para evitar guardados accidentales por GET.

    Espera en el body del POST:
        pub_titulo    — título de la publicación
        pub_categoria — categoría de la publicación
        next          — URL de retorno (opcional)
    """
    if request.method != 'POST':
        return redirect('/')

    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para guardar favoritos.')
        return redirect(request.POST.get('next', '/'))

    pub_titulo = request.POST.get('pub_titulo', '').strip()
    pub_categoria = request.POST.get('pub_categoria', '').strip()

    if not pub_titulo:
        messages.error(request, 'No se pudo identificar la publicación.')
        return redirect(request.POST.get('next', '/'))

    publicacion = {
        'titulo': pub_titulo,
        'categoria': pub_categoria,
    }

    # Verificamos si ya existe el favorito para no duplicar
    # Filtramos en Python para evitar posibles problemas de compatibilidad
    # entre JSONField y djongo en distintas versiones.
    favoritos_existentes = Favorito.objects.all()
    ya_guardado = any(
        f.usuario.get('correo') == usuario['correo']
        and f.publicacion.get('titulo') == pub_titulo
        for f in favoritos_existentes
    )

    if ya_guardado:
        messages.info(request, 'Esta publicación ya está en tus favoritos.')
    else:
        Favorito.objects.create(usuario=usuario, publicacion=publicacion)
        messages.success(request, f'"{pub_titulo}" guardado en favoritos.')

    return redirect(request.POST.get('next', 'interacciones:mis_favoritos'))


def eliminar_favorito(request, favorito_id):
    """
    Elimina un favorito del usuario en sesión.
    Solo permite eliminar favoritos propios.

    Parámetro de URL:
        favorito_id — id del objeto Favorito a eliminar
    """
    if request.method != 'POST':
        return redirect('interacciones:mis_favoritos')

    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión.')
        return redirect('/')

    try:
        favorito = Favorito.objects.get(id=favorito_id)
    except Favorito.DoesNotExist:
        messages.error(request, 'El favorito no existe.')
        return redirect('interacciones:mis_favoritos')

    # Verificamos que el favorito pertenece al usuario en sesion
    if favorito.usuario.get('correo') != usuario.get('correo'):
        messages.error(request, 'No tienes permiso para eliminar este favorito.')
        return redirect('interacciones:mis_favoritos')

    favorito.delete()
    messages.success(request, 'Favorito eliminado.')
    return redirect('interacciones:mis_favoritos')


def mis_favoritos(request):
    """
    Lista todos los favoritos guardados por el usuario en sesion.
    """
    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para ver tus favoritos.')
        return redirect('/')

    # Filtramos en Python por correo del usuario
    todos = Favorito.objects.all()
    favoritos = [
        f for f in todos
        if f.usuario.get('correo') == usuario.get('correo')
    ]

    contexto = {
        'favoritos': favoritos,
        'usuario': usuario,
    }
    return render(request, 'interacciones/mis_favoritos.html', contexto)


# ---------------------------------------------------------------------------
# VISTAS DE COMENTARIOS
# ---------------------------------------------------------------------------

def comentar_publicacion(request):
    """
    Recibe y guarda un comentario sobre una publicación.
    Solo acepta POST.

    Espera en el body del POST los campos del ComentarioForm:
        texto, pub_titulo, pub_categoria
    """
    if request.method != 'POST':
        return redirect('/')

    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para comentar.')
        return redirect(request.POST.get('next', '/'))

    formulario = ComentarioForm(request.POST)

    if formulario.is_valid():
        publicacion = {
            'titulo': formulario.cleaned_data['pub_titulo'],
        }
        if formulario.cleaned_data.get('pub_categoria'):
            publicacion['categoria'] = formulario.cleaned_data['pub_categoria']

        Comentario.objects.create(
            publicacion=publicacion,
            usuario=usuario,
            texto=formulario.cleaned_data['texto'],
        )
        messages.success(request, 'Comentario publicado.')
    else:
        messages.error(request, 'El comentario no es válido. Revisa el texto.')

    # Redirigimos de vuelta a la publicacion de origen
    return redirect(
        request.POST.get('next', 'interacciones:ver_comentarios')
        + f"?pub={request.POST.get('pub_titulo', '')}"
    )


def ver_comentarios(request):
    """
    Lista los comentarios de una publicación específica.

    Query param esperado:
        pub — título de la publicación cuyos comentarios se quieren ver

    También devuelve el formulario para comentar directamente desde esta vista.
    """
    pub_titulo = request.GET.get('pub', '').strip()

    if not pub_titulo:
        messages.error(request, 'No se especificó ninguna publicación.')
        return redirect('/')

    # Filtramos en Python para compatibilidad con djongo + JSONField
    todos = Comentario.objects.filter(estado=Comentario.EstadoComentarioChoices.VISIBLE)
    comentarios = [
        c for c in todos
        if c.publicacion.get('titulo') == pub_titulo
    ]

    formulario = ComentarioForm(initial={
        'pub_titulo': pub_titulo,
    })

    contexto = {
        'comentarios': comentarios,
        'pub_titulo': pub_titulo,
        'formulario': formulario,
        'usuario': services.get_usuario_sesion(request),
    }
    return render(request, 'interacciones/ver_comentarios.html', contexto)


# ---------------------------------------------------------------------------
# VISTA DE DEMO — solo para desarrollo mientras usuarios app no esta lista
# ---------------------------------------------------------------------------

def demo_login(request):
    """
    Vista temporal para simular un login básico durante el desarrollo.
    Debe eliminarse o protegerse antes de producción.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre', 'Usuario Demo')
        correo = request.POST.get('correo', 'demo@universidad.edu')
        services.set_usuario_sesion_demo(request, nombre, correo)
        messages.success(request, f'Sesión iniciada como {nombre}.')
        return redirect('interacciones:mis_favoritos')

    return render(request, 'interacciones/demo_login.html')


def demo_logout(request):
    """
    Cierra la sesión demo.
    """
    request.session.flush()
    messages.info(request, 'Sesión cerrada.')
    return redirect('interacciones:demo_login')



def home(request):
    """
    Página de inicio del Mercadito Universitario.
    Muestra un resumen del estado del proyecto y accesos rápidos.
    Vive en interacciones mientras no haya una app dedicada a esto.
    """
    usuario = services.get_usuario_sesion(request)

    total_comentarios = Comentario.objects.filter(
        estado=Comentario.EstadoComentarioChoices.VISIBLE
    ).count()

    total_favoritos = 0
    if usuario:
        todos = Favorito.objects.all()
        total_favoritos = sum(
            1 for f in todos
            if f.usuario.get('correo') == usuario.get('correo')
        )

    contexto = {
        'usuario': usuario,
        'total_comentarios': total_comentarios,
        'total_favoritos': total_favoritos,
    }
    return render(request, 'interacciones/home.html', contexto)
