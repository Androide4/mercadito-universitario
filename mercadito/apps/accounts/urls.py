from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]