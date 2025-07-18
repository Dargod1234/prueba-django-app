"""
Definiciones de URL para la API REST de la aplicación 'books'.
Gestiona las rutas para los endpoints de la API relacionados con libros y préstamos.
"""
from django.urls import path
from . import api_views

app_name = 'api' # Define el espacio de nombres de la aplicación para URL inversas de la API

urlpatterns = [
    # Endpoints para listar y crear libros (accesible en /api/libros/)
    path('libros/', api_views.LibroListCreateView.as_view(), name='libro-list-create'),
    
    # Endpoints para obtener detalles, actualizar o eliminar un libro específico (accesible en /api/libros/<id>/)
    path('libros/<int:pk>/', api_views.LibroDetailView.as_view(), name='libro-detail'),
    
    # Endpoint para prestar un libro (accesible en /api/libros/<id>/prestar/)
    path('libros/<int:pk>/prestar/', api_views.prestar_libro, name='prestar-libro'),
    
    # Endpoint para devolver un libro (accesible en /api/libros/<id>/devolver/)
    path('libros/<int:pk>/devolver/', api_views.devolver_libro, name='devolver-libro'),
]
