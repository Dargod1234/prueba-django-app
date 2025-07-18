from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    """
    Formulario basado en el modelo Libro para la creación y edición.
    Define los campos del modelo a incluir y aplica clases de Bootstrap
    a los widgets para un diseño consistente.
    """
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'ano_publicacion', 'stock']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
