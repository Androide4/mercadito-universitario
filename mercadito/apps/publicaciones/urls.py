from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_publicaciones, name="listar_publicaciones"),

    path("crear/", views.crear_publicacion, name="crear_publicacion"),

    path("<str:publicacion_id>/editar/", views.editar_publicacion, name="editar_publicacion"),

    path("<str:publicacion_id>/eliminar/", views.eliminar_publicacion, name="eliminar_publicacion"),

    path("<str:publicacion_id>/", views.detalle_publicacion, name="detalle_publicacion"),
]
