from django import forms
from .models import SolicitudIntercambio


class SolicitudIntercambioForm(forms.ModelForm):
    class Meta:
        model = SolicitudIntercambio
        fields = ['mensaje', 'propuesta_intercambio']