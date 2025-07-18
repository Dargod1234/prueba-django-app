from rest_framework import serializers
from .models import Libro, Prestamo, Usuario

class LibroSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Libro.
    Define los campos que se incluyen al serializar/deserializar objetos Libro.
    """
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'ano_publicacion', 'stock']

class PrestamoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Prestamo.
    Permite la representación anidada del libro y la especificación del libro por ID.
    """
    libro = LibroSerializer(read_only=True) # Muestra los detalles completos del libro al leer.
    libro_id = serializers.IntegerField(write_only=True) # Permite especificar el libro por su ID al escribir.
    
    class Meta:
        model = Prestamo
        fields = ['id', 'libro', 'libro_id', 'fecha_prestamo', 'fecha_devolucion', 'activo']
        read_only_fields = ['fecha_prestamo', 'fecha_devolucion'] # Estos campos son gestionados automáticamente.

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    Define los campos básicos del usuario para la API.
    """
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']
