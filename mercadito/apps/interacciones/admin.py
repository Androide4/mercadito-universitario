from django.contrib import admin
from .models import Favorito, Comentario


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('get_usuario', 'get_publicacion', 'fecha_agregado')
    list_filter = ('fecha_agregado',)
    search_fields = ('usuario', 'publicacion')

    def get_usuario(self, obj):
        return obj.usuario.get('nombre', '—')
    get_usuario.short_description = 'Usuario'

    def get_publicacion(self, obj):
        return obj.publicacion.get('titulo', '—')
    get_publicacion.short_description = 'Publicación'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('texto', 'get_usuario', 'get_publicacion', 'estado', 'fecha_comentario')
    list_filter = ('estado', 'fecha_comentario')
    search_fields = ('texto',)
    list_editable = ('estado',)

    def get_usuario(self, obj):
        return obj.usuario.get('nombre', '—')
    get_usuario.short_description = 'Usuario'

    def get_publicacion(self, obj):
        return obj.publicacion.get('titulo', '—')
    get_publicacion.short_description = 'Publicación'
