from django import forms
from .models import SolicitudIntercambio


class SolicitudIntercambioForm(forms.ModelForm):

    titulo_publicacion = forms.CharField(
        max_length=100
    )

    categoria_publicacion = forms.CharField(
        max_length=100
    )

    nombre_solicitante = forms.CharField(
        max_length=100
    )

    correo_solicitante = forms.EmailField()

    class Meta:

        model = SolicitudIntercambio

        fields = [
            'mensaje',
            'propuesta_intercambio'
        ]