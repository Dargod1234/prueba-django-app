from pathlib import Path
from decouple import config, UndefinedValueError # Importamos UndefinedValueError
import dj_database_url

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
    ALLOWED_HOSTS = ['.herokuapp.com', 'your-app-name.herokuapp.com'] # Añade aquí tu dominio personalizado si tienes uno
else:
    # Para desarrollo local, permitir localhost y 127.0.0.1
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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CorsMiddleware en la posición correcta
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware para WhiteNoise (para servir estáticos en producción)
    'whitenoise.middleware.WhiteNoiseMiddleware', 
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
# Configuración de base de datos para desarrollo (desde .env)
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

# Configuración de base de datos para Heroku (producción)
try:
    # Intenta obtener DATABASE_URL. Si no existe, UndefinedValueError será lanzado.
    DATABASE_URL = config('DATABASE_URL')
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600, # Mantener conexiones persistentes por 10 minutos
        ssl_require=True # Requerir SSL para la conexión a la base de datos (común en Heroku)
    )
except UndefinedValueError:
    # Si DATABASE_URL no está definido (estamos en desarrollo o no configurado),
    # simplemente usamos la configuración de base de datos definida arriba.
    pass


# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC' # Se recomienda UTC para consistencia global
USE_I18N = True
USE_TZ = True # Habilita zonas horarias


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Directorio donde Django recolectará los estáticos en producción

# Configuración adicional para servir archivos estáticos con Whitenoise en Heroku
# Si utilizas WhiteNoise, asegúrate de haberlo instalado: pip install whitenoise
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
    # Ejemplo: "https://your-app-name.herokuapp.com",
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

# Configuración para permitir CORS en el Django Admin (opcional, para desarrollo)
# CORS_URLS_REGEX = r"^/admin/.*$" # Si necesitas CORS en el admin