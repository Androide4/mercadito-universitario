import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Publicacion
from .forms import PublicacionForm
from .utils import guardar_imagen
from apps.interacciones import services

def listar_publicaciones(request):
    usuario = services.get_usuario_sesion(request)
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para ver tus favoritos.')
        return redirect('/')
    
    publicaciones = Publicacion.objects.filter(
        estado_publicacion=Publicacion.EstadoPublicacionChoices.ACTIVA
    ).order_by('-fecha_publicacion')
 
    data = {
        "publicaciones": publicaciones,
    }
    return render(request, "listar_publicaciones.html", data)
 

def detalle_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    data = {"publicacion": publicacion}
    return render(request, "detalle_publicacion.html", data)


def crear_publicacion(request):
 
    if request.method == "GET":
        formulario = PublicacionForm()
        return render(request, "crear_publicacion.html", {"formulario": formulario})
    
    formulario = PublicacionForm(request.POST, request.FILES)

    if formulario.is_valid():
        datos = formulario.cleaned_data

        nombre_completo = f"{request.session['usuario_sesion']['nombre']} {request.session['usuario_sesion']['apellido']}"

        autor = {
            "nombre": nombre_completo,
            "correo": request.session['usuario_sesion']['correo'],
            "carrera": request.session.get('usuario_sesion', {}).get('carrera'),
        }

        imagenes = []
        if "imagen" in request.FILES:
            ruta = guardar_imagen(request.FILES["imagen"])
            imagenes.append(ruta)

        Publicacion.objects.create(
            titulo=datos["titulo"],
            descripcion=datos["descripcion"],
            categoria=datos["categoria"],
            tipo_intercambio=datos["tipo_intercambio"],
            precio_referencial=datos.get("precio_referencial"),
            estado_articulo=datos["estado_articulo"],
            estado_publicacion=datos["estado_publicacion"],
            ubicacion_entrega=datos.get("ubicacion_entrega") or None,
            tags=datos["tags"],
            imagenes=imagenes,
            autor=autor,
        )

        messages.success(request, "¡Publicación creada exitosamente!")
        return redirect("listar_publicaciones")

    print(formulario.errors)
    messages.error(request, "Hubo un error al crear la publicación. Por favor, verifica los datos ingresados.")
    return render(request, "crear_publicacion.html", {"formulario": formulario})


def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == "GET":
        datos_iniciales = {
            "titulo": publicacion.titulo,
            "descripcion": publicacion.descripcion,
            "categoria": publicacion.categoria,
            "tipo_intercambio": publicacion.tipo_intercambio,
            "precio_referencial": publicacion.precio_referencial,
            "estado_articulo": publicacion.estado_articulo,
            "estado_publicacion": publicacion.estado_publicacion,
            "ubicacion_entrega": publicacion.ubicacion_entrega,
            "tags": ", ".join(publicacion.tags) if publicacion.tags else "",
        }
        formulario = PublicacionForm(initial=datos_iniciales)
        return render(request, "editar_publicacion.html", {
            "formulario": formulario,
            "publicacion": publicacion,
        })

    formulario = PublicacionForm(request.POST, request.FILES)

    if formulario.is_valid():
        datos = formulario.cleaned_data

        publicacion.titulo = datos["titulo"]
        publicacion.descripcion = datos["descripcion"]
        publicacion.categoria = datos["categoria"]
        publicacion.tipo_intercambio = datos["tipo_intercambio"]
        publicacion.precio_referencial = datos.get("precio_referencial")
        publicacion.estado_articulo = datos["estado_articulo"]
        publicacion.estado_publicacion = datos["estado_publicacion"]
        publicacion.ubicacion_entrega = datos.get("ubicacion_entrega") or None
        publicacion.tags = datos["tags"]

        if "imagen" in request.FILES:
            ruta = guardar_imagen(request.FILES["imagen"])
            imagenes = publicacion.imagenes or []
            imagenes.append(ruta)
            publicacion.imagenes = imagenes

        publicacion.save()
        messages.success(request, "¡Publicación actualizada correctamente!")
        return redirect("detalle_publicacion", publicacion_id=publicacion.id)

    return render(request, "publicaciones/editar_publicacion.html", {
        "formulario": formulario,
        "publicacion": publicacion,
    })

def eliminar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == "POST":
        publicacion.delete()
        messages.success(request, f'La publicación "{publicacion.titulo}" fue eliminada.')
        return redirect("listar_publicaciones")

    return render(request, "eliminar_publicacion.html", {
        "publicacion": publicacion
    })
