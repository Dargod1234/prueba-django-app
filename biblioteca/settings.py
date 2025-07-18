"""
Configuración principal para el proyecto 'biblioteca'.
Contiene ajustes para la base de datos, aplicaciones instaladas, middleware,
archivos estáticos, autenticación y configuración de Django REST Framework.
"""
from pathlib import Path
from decouple import config, UndefinedValueError
import dj_database_url
import os

# Define el directorio base del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para la seguridad de Django. Se obtiene de las variables de entorno.
SECRET_KEY = config('SECRET_KEY')

# Modo de depuración. Se obtiene de las variables de entorno.
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos para servir la aplicación.
ALLOWED_HOSTS = []
if not DEBUG:
    # En producción, se especifican los dominios de la aplicación Heroku.
    ALLOWED_HOSTS = ['.herokuapp.com', 'prueba-django-2db3239ec097.herokuapp.com']
    # Si se usa un dominio personalizado, se añadiría aquí: ALLOWED_HOSTS.append('tu-dominio.com')
else:
    # En desarrollo local, se permiten localhost y 127.0.0.1.
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Definición de las aplicaciones instaladas en el proyecto.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Django REST Framework
    'corsheaders',    # Para manejar CORS en la API
    'books',          # Tu aplicación principal
]

# Middleware utilizado para procesar solicitudes y respuestas.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',      # Debe ir después de SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLconf raíz del proyecto.
ROOT_URLCONF = 'biblioteca.urls'

# Configuración de los motores de plantillas.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Directorio para plantillas globales del proyecto
        'APP_DIRS': True, # Permite a las aplicaciones buscar sus propias plantillas
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Punto de entrada WSGI para servidores de producción.
WSGI_APPLICATION = 'biblioteca.wsgi.application'

# Configuración de la base de datos.
# Maneja la configuración dual para Heroku (DATABASE_URL) y desarrollo local (.env).
try:
    # Intenta obtener DATABASE_URL (existirá en Heroku).
    DATABASE_URL = config('DATABASE_URL')
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600, # Mantener conexiones persistentes por 10 minutos
            ssl_require=True  # Requerir SSL para la conexión a la base de datos (común en Heroku)
        )
    }
except UndefinedValueError:
    # Si DATABASE_URL no está definido (desarrollo local), usa las variables del archivo .env.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }


# Configuración de internacionalización.
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC' # Se recomienda UTC para consistencia global en fechas y horas.
USE_I18N = True   # Habilita el sistema de traducción de Django.
USE_TZ = True     # Habilita el soporte para zonas horarias.


# Configuración de archivos estáticos (CSS, JavaScript, Imágenes).
STATIC_URL = '/static/'
# Directorio donde Django recolectará todos los archivos estáticos en producción.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de almacenamiento de archivos estáticos para WhiteNoise.
# Asegúrate de haber instalado WhiteNoise (pip install whitenoise).
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Tipo de campo de clave primaria por defecto para los modelos.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Modelo de usuario personalizado.
AUTH_USER_MODEL = 'books.Usuario'

# URLs de login y logout para el sistema de autenticación de Django.
LOGIN_URL = 'books:login' # Nombre de la URL para el login.
LOGIN_REDIRECT_URL = 'books:listar_libros' # Redirección después de login exitoso.
LOGOUT_REDIRECT_URL = 'books:listar_libros' # Redirección después de logout exitoso.

# Configuración de CORS Headers.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Agrega aquí los orígenes de tu frontend si están en otro puerto (ej. React, Vue, Angular).
    # "http://localhost:3000",
    # "http://127.0.0.1:3000",
    # URL de tu aplicación Heroku para permitir solicitudes CORS desde tu propio despliegue.
    "https://prueba-django-2db3239ec097.herokuapp.com", 
]

# Configuración de Django REST Framework.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # Puedes añadir 'rest_framework.authentication.TokenAuthentication' si implementas tokens.
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Permiso global por defecto: permite lectura a todos, escritura solo a autenticados.
        # Las vistas específicas de la API sobrescriben esto con permisos más granulares.
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', 
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # Útil para depuración en el navegador.
    ],
}
