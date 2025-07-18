"""
Configuración WSGI para el proyecto 'biblioteca'.

Expone el objeto invocable WSGI como una variable a nivel de módulo llamada `application`.
Este archivo es el punto de entrada para servidores web compatibles con WSGI (como Gunicorn).
"""

import os

from django.core.wsgi import get_wsgi_application

# Establece la variable de entorno para el módulo de configuración de Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')

# Obtiene la aplicación WSGI de Django.
application = get_wsgi_application()
