"""
Configuración de URL principal para el proyecto 'biblioteca'.
Define las rutas a nivel de proyecto, incluyendo el admin de Django,
las URLs de la aplicación 'books' y las URLs de la API REST.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # URLs para el panel de administración de Django
    path('', include('books.urls')), # Incluye las URLs de la aplicación 'books' (vistas web)
    path('api/', include('books.api_urls')), # Incluye las URLs de la API REST
]
