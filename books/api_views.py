from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes # <--- IMPORTANTE: 'permission_classes' debe venir de 'decorators'
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Libro, Prestamo
from .serializers import LibroSerializer, PrestamoSerializer # Asumiendo que PrestamoSerializer también se usa si se expande la API
from .permissions import IsAdminUserOrReadOnly, IsRegularUser

class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    # perform_create puede usarse para asignar el usuario que crea el libro,
    # si el modelo Libro tuviera un campo para ello (ej. 'creado_por').
    # Si no tienes esa lógica, esta sección puede omitirse o mantenerse como un recordatorio.
    # def perform_create(self, serializer):
    #     serializer.save(creado_por=self.request.user)

class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    # perform_update y perform_destroy se mantienen solo si hay lógica adicional
    # más allá de la validación de permisos, como la gestión de stock en el modelo.
    # La lógica de permisos de rol ya está cubierta por IsAdminUserOrReadOnly.
    # def perform_update(self, serializer):
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     instance.delete()

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRegularUser])
def prestar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    
    # Verificar si ya tiene el libro prestado activamente por este usuario
    prestamo_activo = Prestamo.objects.filter(
        usuario=request.user, 
        libro=libro, 
        activo=True
    ).exists()
    
    if prestamo_activo:
        return Response(
            {'error': 'Ya tienes este libro prestado. Por favor, devuélvelo antes de intentar prestarlo de nuevo.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if libro.stock > 0:
        Prestamo.objects.create(usuario=request.user, libro=libro, activo=True)
        libro.stock -= 1
        libro.save()
        
        return Response(
            {'message': f'Has prestado "{libro.titulo}" exitosamente.'}, 
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {'error': 'No hay stock disponible para este libro.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRegularUser])
def devolver_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    
    try:
        # Busca el préstamo ACTIVO que el usuario tiene para este libro
        prestamo = Prestamo.objects.get(
            usuario=request.user, 
            libro=libro, 
            activo=True
        )
        
        prestamo.fecha_devolucion = timezone.now()
        prestamo.activo = False
        prestamo.save()
        
        libro.stock += 1
        libro.save()
        
        return Response(
            {'message': f'Has devuelto "{libro.titulo}" exitosamente.'}, 
            status=status.HTTP_200_OK
        )
    except Prestamo.DoesNotExist:
        # Si no se encuentra un préstamo activo, significa que el libro no está prestado
        # o ya ha sido devuelto por este usuario.
        return Response(
            {'error': 'Este libro no está prestado por ti o ya ha sido devuelto.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )