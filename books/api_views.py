from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Libro, Prestamo
from .serializers import LibroSerializer, PrestamoSerializer
from .permissions import IsAdminUserOrReadOnly, IsRegularUser

class LibroListCreateView(generics.ListCreateAPIView):
    """
    Vista de API para listar todos los libros y crear nuevos libros.
    Permite lectura a todos, pero la creación está restringida a usuarios administradores.
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista de API para recuperar, actualizar o eliminar un libro específico.
    Permite lectura a todos, pero la actualización y eliminación están restringidas a administradores.
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUserOrReadOnly]

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRegularUser])
def prestar_libro(request, pk: int):
    """
    Endpoint de API para que un usuario regular preste un libro.
    Requiere autenticación y rol 'regular'.
    """
    libro = get_object_or_404(Libro, pk=pk)
    
    # Verifica si el usuario ya tiene este libro prestado activamente.
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
        # Crea un nuevo registro de préstamo con estado activo.
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
def devolver_libro(request, pk: int):
    """
    Endpoint de API para que un usuario regular devuelva un libro.
    Requiere autenticación y rol 'regular'.
    """
    libro = get_object_or_404(Libro, pk=pk)
    
    try:
        # Busca el préstamo activo que el usuario tiene para este libro.
        prestamo = Prestamo.objects.get(
            usuario=request.user, 
            libro=libro, 
            activo=True
        )
        
        prestamo.fecha_devolucion = timezone.now()
        prestamo.activo = False # Marca el préstamo como inactivo.
        prestamo.save()
        
        libro.stock += 1
        libro.save()
        
        return Response(
            {'message': f'Has devuelto "{libro.titulo}" exitosamente.'}, 
            status=status.HTTP_200_OK
        )
    except Prestamo.DoesNotExist:
        # Si no se encuentra un préstamo activo, el libro no está prestado o ya ha sido devuelto.
        return Response(
            {'error': 'Este libro no está prestado por ti o ya ha sido devuelto.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
