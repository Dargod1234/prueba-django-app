"""
Configuración ASGI para el proyecto 'biblioteca'.

Expone el objeto invocable ASGI como una variable a nivel de módulo llamada `application`.
Este archivo es el punto de entrada para servidores web compatibles con ASGI (como Daphne o Uvicorn),
permitiendo funcionalidades asíncronas como WebSockets.
"""

import os

from django.core.asgi import get_asgi_application

# Establece la variable de entorno para el módulo de configuración de Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')

# Obtiene la aplicación ASGI de Django.
application = get_asgi_application()
