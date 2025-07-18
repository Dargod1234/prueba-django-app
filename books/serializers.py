from rest_framework import serializers
from .models import Libro, Prestamo, Usuario

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'ano_publicacion', 'stock']

class PrestamoSerializer(serializers.ModelSerializer):
    libro = LibroSerializer(read_only=True)
    libro_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Prestamo
        fields = ['id', 'libro', 'libro_id', 'fecha_prestamo', 'fecha_devolucion', 'activo']
        read_only_fields = ['fecha_prestamo', 'fecha_devolucion']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']