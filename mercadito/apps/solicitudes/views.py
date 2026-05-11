from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import SolicitudIntercambio
from .forms import SolicitudIntercambioForm


def enviar_solicitud(request):

    if request.method == 'POST':

        form = SolicitudIntercambioForm(request.POST)

        if form.is_valid():

            solicitud = form.save(commit=False)

            solicitud.publicacion = {
                "titulo": form.cleaned_data['titulo_publicacion'],
                "categoria": form.cleaned_data['categoria_publicacion']
            }

            solicitud.solicitante = {
                "nombre": form.cleaned_data['nombre_solicitante'],
                "correo": form.cleaned_data['correo_solicitante']
            }

            solicitud.save()

            return redirect('lista_solicitudes')

    else:

        form = SolicitudIntercambioForm()

    return render(
        request,
        'solicitudes/enviar_solicitud.html',
        {'form': form}
    )


def lista_solicitudes(request):

    solicitudes = SolicitudIntercambio.objects.all()

    return render(
        request,
        'solicitudes/lista_solicitudes.html',
        {'solicitudes': solicitudes}
    )


def aceptar_solicitud(request, solicitud_id):

    solicitud = get_object_or_404(
        SolicitudIntercambio,
        id=solicitud_id
    )

    solicitud.estado_solicitud = 'aceptada'
    solicitud.fecha_respuesta = timezone.now()

    solicitud.save()

    return redirect('lista_solicitudes')


def rechazar_solicitud(request, solicitud_id):

    solicitud = get_object_or_404(
        SolicitudIntercambio,
        id=solicitud_id
    )

    solicitud.estado_solicitud = 'rechazada'
    solicitud.fecha_respuesta = timezone.now()

    solicitud.save()

    return redirect('lista_solicitudes')


def cancelar_solicitud(request, solicitud_id):

    solicitud = get_object_or_404(
        SolicitudIntercambio,
        id=solicitud_id
    )

    solicitud.estado_solicitud = 'cancelada'

    solicitud.save()

    return redirect('lista_solicitudes')