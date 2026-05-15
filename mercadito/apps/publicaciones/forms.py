from django import forms
from .models import Publicacion


class PublicacionForm(forms.Form):
    titulo = forms.CharField(
        label="Título del artículo",
        max_length=100,
        min_length=3,
        widget=forms.TextInput(attrs={
            "placeholder": "Ej: Libro de Cálculo Integral",
            "class": "form-control"
        })
    )

    descripcion = forms.CharField(
        label="Descripción",
        min_length=10,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Describe el estado, características y detalles del artículo...",
            "class": "form-control"
        })
    )

    categoria = forms.ChoiceField(
        label="Categoría",
        choices=Publicacion.CategoriaChoices.choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    tipo_intercambio = forms.ChoiceField(
        label="Tipo de publicación",
        choices=Publicacion.TipoIntercambioChoices.choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    precio_referencial = forms.DecimalField(
        label="Precio referencial (opcional)",
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "placeholder": "0.00",
            "class": "form-control",
            "step": "0.01"
        })
    )

    estado_articulo = forms.ChoiceField(
        label="Estado del artículo",
        choices=Publicacion.EstadoArticuloChoices.choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    estado_publicacion = forms.ChoiceField(
        label="Estado de la publicación",
        choices=Publicacion.EstadoPublicacionChoices.choices,
        initial=Publicacion.EstadoPublicacionChoices.ACTIVA,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    ubicacion_entrega = forms.CharField(
        label="Lugar de entrega / intercambio (opcional)",
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Ej: Biblioteca central, Bloque B",
            "class": "form-control"
        })
    )

    tags = forms.CharField(
        label="Palabras clave (separadas por coma)",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Ej: calculo, matematicas, ingenieria",
            "class": "form-control"
        })
    )

    # Campo para subir imagen (opcional)
    imagen = forms.ImageField(
        label="Imagen del artículo (opcional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )


    def clean_tags(self):
        """
        Convierte el string de tags separados por coma en una lista limpia.
        Ejemplo: "calculo, matematicas, ingenieria" → ["calculo", "matematicas", "ingenieria"]
        """
        tags_raw = self.cleaned_data.get("tags", "")
        if not tags_raw:
            return []
        return [tag.strip().lower() for tag in tags_raw.split(",") if tag.strip()]

    def clean(self):
        """
        Validación cruzada: si el tipo es 'venta', el precio referencial
        es recomendable aunque no obligatorio.
        """
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo_intercambio")
        precio = cleaned_data.get("precio_referencial")

        if tipo == "venta" and not precio:
            # Solo advertencia visual — no bloqueamos el envío
            self.add_error(
                "precio_referencial",
                "Se recomienda indicar un precio cuando el tipo es 'Venta'."
            )
        return cleaned_data
