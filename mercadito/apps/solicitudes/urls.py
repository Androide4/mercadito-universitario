from django.urls import path
from . import views

urlpatterns = [

    path(
        'enviar/<str:publicacion_id>/',
        views.enviar_solicitud,
        name='enviar_solicitud'
    ),

    path(
        'lista/',
        views.lista_solicitudes,
        name='lista_solicitudes'
    ),

    path(
        'aceptar/<str:solicitud_id>/',
        views.aceptar_solicitud,
        name='aceptar_solicitud'
    ),

    path(
        'rechazar/<str:solicitud_id>/',
        views.rechazar_solicitud,
        name='rechazar_solicitud'
    ),

    path(
        'cancelar/<str:solicitud_id>/',
        views.cancelar_solicitud,
        name='cancelar_solicitud'
    ),

    path(
        'responder/<str:solicitud_id>/',
        views.responder_solicitud,
        name='responder_solicitud'
    ),
]