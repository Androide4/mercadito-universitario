from django.urls import path
from . import views

app_name = 'interacciones'

urlpatterns = [
    # --- Pagina de inicio ---
    path('home/', views.home, name='home'),

    # --- Favoritos ---
    path('favoritos/', views.mis_favoritos, name='mis_favoritos'),
    path('favoritos/guardar/', views.guardar_favorito, name='guardar_favorito'),
    path('favoritos/eliminar/<str:favorito_id>/', views.eliminar_favorito, name='eliminar_favorito'),

    # --- Comentarios ---
    path('comentarios/', views.ver_comentarios, name='ver_comentarios'),
    path('comentarios/nuevo/', views.comentar_publicacion, name='comentar_publicacion'),

    # --- Demo (solo desarrollo) ---
    path('demo/login/', views.demo_login, name='demo_login'),
    path('demo/logout/', views.demo_logout, name='demo_logout'),
]
