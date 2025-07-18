from pathlib import Path
from decouple import config, UndefinedValueError
import dj_database_url
import os # Importar os para la compatibilidad con el entorno de Heroku para el static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []
if not DEBUG:
    # Para producción, debes especificar los hosts permitidos.
    # Heroku usa su propio dominio.
    # Reemplaza 'your-app-name.herokuapp.com' con el nombre real de tu app de Heroku.
    ALLOWED_HOSTS = ['.herokuapp.com', 'prueba-django-2db3239ec097.herokuapp.com'] # Asegúrate de que este sea el nombre de tu app Heroku
else:
    # Para desarrollo local
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'books', # Tu aplicación 'books'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise debe ir después de SecurityMiddleware para servir estáticos de forma segura
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CorsMiddleware en la posición correcta
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'biblioteca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Asegúrate de que tu carpeta de templates globales esté aquí
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'biblioteca.wsgi.application'

# Database
# Configuración para Heroku y desarrollo local (manejo dual)
try:
    # Intenta obtener DATABASE_URL (esto existirá en Heroku)
    DATABASE_URL = config('DATABASE_URL')
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600, # Mantener conexiones persistentes por 10 minutos
            ssl_require=True # Requerir SSL para la conexión a la base de datos (común en Heroku)
        )
    }
except UndefinedValueError:
    # Si DATABASE_URL no está definido (estamos en desarrollo local),
    # usamos las variables del archivo .env para PostgreSQL local.
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


# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC' # Se recomienda UTC para consistencia global
USE_I18N = True
USE_TZ = True # Habilita zonas horarias


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# Directorio donde Django recolectará los estáticos en producción.
# Esto es donde WhiteNoise buscará los archivos.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración adicional para servir archivos estáticos con Whitenoise en Heroku
# Asegúrate de haber instalado WhiteNoise: pip install whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'books.Usuario'

# URL de login y logout (para @login_required y LoginRequiredMixin)
LOGIN_URL = 'books:login' # Nombre de la URL para el login
LOGIN_REDIRECT_URL = 'books:listar_libros' # A dónde ir después de un login exitoso
LOGOUT_REDIRECT_URL = 'books:listar_libros' # A dónde ir después de un logout exitoso

# CORS Headers configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Agrega aquí los orígenes de tu frontend si están en otro puerto (ej. React, Vue, Angular)
    # "http://localhost:3000",
    # "http://127.0.0.1:3000",
    # Cuando despliegues en Heroku, añade la URL de tu aplicación.
    "https://prueba-django.herokuapp.com", # Asegúrate de que este sea el nombre de tu app Heroku
]

# Si prefieres permitir cualquier origen durante el desarrollo (MENOS SEGURO PARA PRODUCCIÓN)
# CORS_ALLOW_ALL_ORIGINS = DEBUG


# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # Puedes añadir TokenAuthentication aquí si lo implementas más adelante
        # 'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Esto es un permiso global por defecto.
        # En tus vistas (api_views.py), estás sobrescribiendo esto con permisos más específicos,
        # lo cual es la mejor práctica.
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}