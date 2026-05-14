from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Favorito, Comentario
from .forms import ComentarioForm
from . import services


# ─────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────

def home(request):
    usuario = services.get_usuario_sesion(request)
    publicaciones = services.get_publicaciones_activas(limite=8)

    total_comentarios = Comentario.objects.filter(
        estado=Comentario.EstadoComentarioChoices.VISIBLE
    ).count()

    total_favoritos = 0
    if usuario:
        total_favoritos = sum(
            1 for f in Favorito.objects.all()
            if f.usuario.get('correo') == usuario.get('correo')
        )

    return render(request, 'interacciones/home.html', {
        'usuario': usuario,
        'publicaciones': publicaciones,
        'total_comentarios': total_comentarios,
        'total_favoritos': total_favoritos,
    })


# ─────────────────────────────────────────────
# FAVORITOS
# ─────────────────────────────────────────────

def guardar_favorito(request):
    if request.method != 'POST':
        return redirect('interacciones:home')

    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para guardar favoritos.')
        return redirect('login')

    pub_titulo    = request.POST.get('pub_titulo', '').strip()
    pub_categoria = request.POST.get('pub_categoria', '').strip()
    pub_id        = request.POST.get('pub_id', '').strip()
    next_url      = request.POST.get('next', '/')

    if not pub_titulo:
        messages.error(request, 'No se pudo identificar la publicación.')
        return redirect(next_url)

    # Verificar duplicado
    ya_guardado = any(
        f.usuario.get('correo') == usuario['correo']
        and f.publicacion.get('titulo') == pub_titulo
        for f in Favorito.objects.all()
    )

    if ya_guardado:
        messages.info(request, 'Esta publicación ya está en tus favoritos.')
    else:
        Favorito.objects.create(
            usuario={
                'id':      usuario.get('id', ''),
                'nombre':  usuario.get('nombre', ''),
                'correo':  usuario['correo'],
            },
            publicacion={
                'id':        pub_id,
                'titulo':    pub_titulo,
                'categoria': pub_categoria,
            },
        )
        messages.success(request, f'"{pub_titulo}" guardado en favoritos.')

    return redirect(next_url)


def eliminar_favorito(request, favorito_id):
    if request.method != 'POST':
        return redirect('interacciones:mis_favoritos')

    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión.')
        return redirect('login')

    try:
        favorito = Favorito.objects.get(id=favorito_id)
    except Favorito.DoesNotExist:
        messages.error(request, 'El favorito no existe.')
        return redirect('interacciones:mis_favoritos')

    if favorito.usuario.get('correo') != usuario.get('correo'):
        messages.error(request, 'No tienes permiso para eliminar este favorito.')
        return redirect('interacciones:mis_favoritos')

    favorito.delete()
    messages.success(request, 'Favorito eliminado.')
    return redirect('interacciones:mis_favoritos')


def mis_favoritos(request):
    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para ver tus favoritos.')
        return redirect('login')

    favoritos = [
        f for f in Favorito.objects.all()
        if f.usuario.get('correo') == usuario.get('correo')
    ]

    return render(request, 'interacciones/mis_favoritos.html', {
        'favoritos': favoritos,
        'usuario': usuario,
    })


# ─────────────────────────────────────────────
# COMENTARIOS
# ─────────────────────────────────────────────

def comentar_publicacion(request):
    if request.method != 'POST':
        return redirect('interacciones:home')

    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para comentar.')
        return redirect('login')

    formulario = ComentarioForm(request.POST)
    next_url = request.POST.get('next', '/')

    if formulario.is_valid():
        publicacion = {'titulo': formulario.cleaned_data['pub_titulo']}
        if formulario.cleaned_data.get('pub_categoria'):
            publicacion['categoria'] = formulario.cleaned_data['pub_categoria']

        Comentario.objects.create(
            publicacion=publicacion,
            usuario={
                'id':      usuario.get('id', ''),
                'nombre':  usuario.get('nombre', ''),
                'correo':  usuario['correo'],
                'carrera': usuario.get('carrera', ''),
            },
            texto=formulario.cleaned_data['texto'],
        )
        messages.success(request, 'Comentario publicado.')
    else:
        messages.error(request, 'El comentario no es válido. Mínimo 2 caracteres.')

    return redirect(next_url)


def ver_comentarios(request):
    pub_titulo = request.GET.get('pub', '').strip()

    if not pub_titulo:
        messages.error(request, 'No se especificó ninguna publicación.')
        return redirect('interacciones:home')

    comentarios = [
        c for c in Comentario.objects.filter(
            estado=Comentario.EstadoComentarioChoices.VISIBLE
        )
        if c.publicacion.get('titulo') == pub_titulo
    ]

    return render(request, 'interacciones/ver_comentarios.html', {
        'comentarios': comentarios,
        'pub_titulo':  pub_titulo,
        'formulario':  ComentarioForm(initial={'pub_titulo': pub_titulo}),
        'usuario':     services.get_usuario_sesion(request),
    })


# ─────────────────────────────────────────────
# DEMO — eliminar cuando accounts esté listo
# ─────────────────────────────────────────────

def demo_login(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', 'Usuario Demo')
        correo = request.POST.get('correo', 'demo@universidad.edu')
        services.set_usuario_sesion_demo(request, nombre, correo)
        messages.success(request, f'Sesión iniciada como {nombre}.')
        return redirect('interacciones:home')
    return render(request, 'interacciones/demo_login.html')


def demo_logout(request):
    request.session.flush()
    messages.info(request, 'Sesión cerrada.')
    return redirect('interacciones:home')