from django import forms
from .models import Usuario


class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña'
        })
    )
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellido',
            'correo',
            'password',
            'carrera',
            'semestre',
            'telefono',
            'descripcion',
            'foto_perfil'
        ]