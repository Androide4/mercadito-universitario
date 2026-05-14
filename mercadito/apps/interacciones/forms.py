from django import forms


class ComentarioForm(forms.Form):
    """
    Formulario para crear un comentario sobre una publicación.
    Hereda de forms.Form (no ModelForm) para mantener control manual
    sobre la creación del objeto y el manejo del JSONField de usuario/publicación.
    """
    texto = forms.CharField(
        label="Comentario",
        min_length=2,
        max_length=300,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Escribe tu comentario (máx. 300 caracteres)...',
            'class': 'form-textarea',
        })
    )

    # Campos ocultos que viajan desde el template de publicaciones
    pub_titulo = forms.CharField(widget=forms.HiddenInput())
    pub_categoria = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
