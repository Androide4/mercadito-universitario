from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import SolicitudIntercambio
from .forms import SolicitudIntercambioForm
from apps.publicaciones.models import Publicacion
from apps.interacciones import services


def enviar_solicitud(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    usuario_sesion = services.get_usuario_sesion(request)

    if not usuario_sesion:
        return redirect('login')

    if request.method == 'POST':
        form = SolicitudIntercambioForm(request.POST)

        if form.is_valid():
            solicitud = form.save(commit=False)

            solicitud.publicacion = {
                "id": str(publicacion.id),
                "titulo": publicacion.titulo,
                "categoria": publicacion.get_categoria_display()
            }

            nombre_completo = f"{request.session['usuario_sesion']['nombre']} {request.session['usuario_sesion']['apellido']}"

            solicitud.solicitante = {
                "id": str(usuario_sesion.get('id')),
                "nombre": nombre_completo,
                "correo": usuario_sesion.get('correo')
            }

            solicitud.save()
            return redirect('lista_solicitudes')
    else:
        form = SolicitudIntercambioForm()

    return render(request, 'solicitudes/enviar_solicitud.html', {
        'form': form,
        'publicacion': publicacion,
        'tipo': publicacion.tipo_intercambio
    })

def lista_solicitudes(request):
    usuario_sesion = services.get_usuario_sesion(request)

    if not usuario_sesion:
        return redirect('login')

    from apps.publicaciones.models import Publicacion

    correo = usuario_sesion.get('correo')

    mis_publicaciones_ids = {
        str(p.id) for p in Publicacion.objects.all()
        if p.autor.get('correo') == correo
    }

    todas = SolicitudIntercambio.objects.all()

    # Las que llegaron a mis publicaciones
    recibidas = [s for s in todas if s.publicacion.get('id') in mis_publicaciones_ids]

    # Las que yo envié
    enviadas = [s for s in todas if s.solicitante.get('correo') == correo]

    return render(
        request,
        'solicitudes/lista_solicitudes.html',
        {
            'recibidas': recibidas,
            'enviadas': enviadas,
            'usuario': usuario_sesion,
        }
    )

def aceptar_solicitud(request, solicitud_id):
    from apps.publicaciones.models import Publicacion

    solicitud = get_object_or_404(SolicitudIntercambio, id=solicitud_id)

    try:
        pub_id = solicitud.publicacion.get('id')
        publicacion = Publicacion.objects.get(id=pub_id)
        if publicacion.estado_publicacion == 'cerrada':
            return redirect('lista_solicitudes')
    except Exception:
        pass

    solicitud.estado_solicitud = 'aceptada'
    solicitud.fecha_respuesta = timezone.now()
    solicitud.save()

    try:
        publicacion.estado_publicacion = 'cerrada'
        publicacion.save()
    except Exception:
        pass

    return redirect('responder_solicitud', solicitud_id=solicitud_id)


def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudIntercambio, id=solicitud_id)
    solicitud.estado_solicitud = 'rechazada'
    solicitud.fecha_respuesta = timezone.now()
    solicitud.save()
    return redirect('responder_solicitud', solicitud_id=solicitud_id)

def cancelar_solicitud(request, solicitud_id):
    usuario_sesion = services.get_usuario_sesion(request)

    if not usuario_sesion:
        return redirect('login')

    solicitud = get_object_or_404(SolicitudIntercambio, id=solicitud_id)

    if solicitud.solicitante.get('correo') != usuario_sesion.get('correo'):
        return HttpResponseForbidden("No puedes cancelar esta solicitud.")

    solicitud.delete()
    return redirect('lista_solicitudes')

def responder_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudIntercambio, id=solicitud_id)

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta', '').strip()
        if respuesta:
            solicitud.respuesta = respuesta
            solicitud.save()
        return redirect('lista_solicitudes')

    return render(request, 'solicitudes/responder_solicitud.html', {
        'solicitud': solicitud
    })