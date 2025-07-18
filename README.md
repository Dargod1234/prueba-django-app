# Sistema de Gestión de Biblioteca - Prueba Técnica Django

## Descripción del Proyecto

Aplicación web backend desarrollada con **Django** y **Django REST Framework (DRF)** para la gestión de una biblioteca. Permite administrar libros y usuarios, incluyendo funcionalidades de autenticación, préstamos y devoluciones. La aplicación está diseñada para ser desplegada en **Heroku** y expone una API REST para interactuar con los recursos.

---

## Características Implementadas

### ✅ Funcionalidades Principales (Web & API)

* **Modelos de Datos:**
    * **Libro:** Título, autor, año de publicación, cantidad en stock.
    * **Usuario:** Nombre de usuario, correo electrónico, rol (`regular` o `admin`).
    * **Préstamo:** Relación de muchos a muchos entre `Usuario` y `Libro` para gestionar los libros prestados.
* **Gestión de Libros:**
    * Listado de todos los libros disponibles.
    * Visualización de detalles de un libro específico.
    * Creación y edición de libros (solo para `administradores`).
    * Funcionalidad para tomar prestado y devolver un libro (solo para `usuarios regulares`).
    * Listado de libros prestados y devueltos por un `usuario regular`.
* **Sistema de Autenticación:**
    * Login y Logout de usuarios.
    * Protección de rutas y endpoints de API basada en autenticación y roles.

### ✅ API REST (Django REST Framework)

* **Endpoints de Libros:**
    * `GET /api/libros/`: Listar todos los libros.
    * `GET /api/libros/<id>/`: Ver detalles de un libro específico.
    * `POST /api/libros/`: Crear un nuevo libro (solo `administradores` autenticados).
    * `PUT /api/libros/<id>/`: Editar un libro existente (solo `administradores` autenticados).
    * `DELETE /api/libros/<id>/`: Eliminar un libro (solo `administradores` autenticados).
* **Endpoints de Préstamos:**
    * `POST /api/libros/<id>/prestar/`: Tomar prestado un libro (solo `usuarios regulares` autenticados).
    * `POST /api/libros/<id>/devolver/`: Devolver un libro (solo `usuarios regulares` autenticados).
* **Permisos y Autenticación:**
    * Uso de `SessionAuthentication` y `BasicAuthentication` para el acceso a la API.
    * Implementación de permisos personalizados en DRF para controlar el acceso según el rol del usuario (`IsAdminUser` o `IsRegularUser`).

### ✅ Despliegue

* Aplicación desplegada en **Heroku**.
* Configuración de servidor **PostgreSQL** como base de datos en Heroku.
* Servicio de archivos estáticos configurado con **WhiteNoise**.

---

## Tecnologías Utilizadas

* **Django 5.x**: Framework principal de desarrollo web.
* **Django REST Framework 3.x**: Para la construcción de la API RESTful.
* **Python 3.12+**: Lenguaje de programación.
* **PostgreSQL**: Sistema de gestión de bases de datos.
* **dj-database-url**: Para la configuración de la base de datos en entornos.
* **python-decouple**: Para la gestión de variables de entorno.
* **Gunicorn**: Servidor WSGI para producción en Heroku.
* **WhiteNoise**: Para servir archivos estáticos de forma eficiente en producción.
* **django-cors-headers**: Para la gestión de Cross-Origin Resource Sharing (CORS) en la API.
* **Git**: Control de versiones.
* **Heroku**: Plataforma de despliegue.

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes elementos en tu sistema:

* **Python 3.12+**
* **pip** (gestor de paquetes de Python)
* **Git**
* **Heroku CLI** (para el despliegue)
* **PostgreSQL** (opcional, si deseas correr la base de datos localmente, de lo contrario, puedes usar SQLite para desarrollo o confiar solo en Heroku Postgres).

---

## Instalación y Configuración (Local)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Dargod1234/prueba-django-app.git
cd nombre-del-directorio-de-tu-proyecto
```

### 2. Crear y activar el entorno virtual

Es crucial trabajar con un entorno virtual para gestionar las dependencias del proyecto.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS (o Git Bash en Windows):**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

Con el entorno virtual activado, instala todas las librerías necesarias desde requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz de tu proyecto (al mismo nivel que manage.py).

```env
# .env
SECRET_KEY=tu_clave_secreta_aqui_genera_una_nueva
DEBUG=True

# Configuración de base de datos PostgreSQL local
DB_NAME=nombre_de_tu_bd
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

**SECRET_KEY:** Genera una clave secreta segura con `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

Ajusta los valores de `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` según tu configuración local de PostgreSQL.

### 5. Ejecutar migraciones

Aplica las migraciones de la base de datos:

```bash
python manage.py migrate
```

### 6. Crear un superusuario (opcional, para acceder al admin de Django)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario admin.

---

## Ejecución del Proyecto (Local)

### Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en http://localhost:8000.

- **Panel de Administración de Django:** http://localhost:8000/admin/
- **API Root (Browsable API):** http://localhost:8000/api/

---

## Despliegue en Heroku

La aplicación está configurada para ser desplegada en Heroku.

### Pre-requisitos de Heroku:
- Cuenta Heroku verificada (con método de pago configurado, aunque el plan sea gratuito).
- Heroku CLI instalado y haber iniciado sesión (`heroku login`).

### Pasos del Despliegue:

1. **Crear la aplicación Heroku:** (Si aún no la has creado)

```bash
heroku create nombre-de-tu-app-unica # Ej: heroku create mi-biblioteca-django
```

2. **Configurar variables de entorno en Heroku:**

```bash
heroku config:set SECRET_KEY='tu_nueva_clave_secreta_PARA_HEROKU'
heroku config:set DEBUG=False
```

¡Importante! Usa una nueva `SECRET_KEY` para producción diferente a la de desarrollo.
`DEBUG=False` es crucial para la seguridad en producción.

3. **Añadir el complemento de base de datos PostgreSQL:**

```bash
heroku addons:create heroku-postgresql:essential-0
```

Esto provisionará una base de datos PostgreSQL y establecerá automáticamente la variable de entorno `DATABASE_URL`.

4. **Desplegar el código a Heroku:**

```bash
git push heroku master
```

(Asegúrate de que `master` sea el nombre de tu rama principal).

5. **Ejecutar migraciones en Heroku:**

```bash
heroku run python manage.py migrate
```

6. **Recolectar archivos estáticos en Heroku:**

```bash
heroku run python manage.py collectstatic
```

7. **Crear un superusuario en Heroku (para acceder al admin de tu app desplegada):**

```bash
heroku run python manage.py createsuperuser
```

8. **Acceder a la aplicación desplegada:**

```bash
heroku open
```

Esto abrirá tu aplicación en el navegador.

---

## Credenciales para Acceso (Para Revisión)

Para acceder a las funcionalidades protegidas (como la administración o probar diferentes roles):

**Usuario Administrador:**
- Username: `admin`
- Password: `holamundo` 

**Usuario Regular:**
- Username: `usuario1`
- Password: `holamundo` 

**URL de la Aplicación Desplegada:**
https://prueba-django-2db3239ec097.herokuapp.com/


---

## Documentación y Pruebas de API con Postman (Opcional)

Si has completado esta parte:

**Colección de Postman:** Incluye el archivo JSON de tu colección de Postman en la raíz de este repositorio, nombrado `biblioteca_api_postman_collection.json`.

**Endpoints Clave:**
- Login (POST `/api/login/` - usar credenciales admin/regular para obtener sesión).
- Listar Libros (GET `/api/libros/`).
- Crear Libro (POST `/api/libros/` - requiere autenticación admin).
- Tomar Prestado (POST `/api/libros/<id>/prestar/` - requiere autenticación regular).
- Devolver Libro (POST `/api/libros/<id>/devolver/` - requiere autenticación regular).

---

## Pruebas (Opcional)

Si has implementado pruebas, se encuentran en el directorio `[nombre_de_tu_app]/tests/`.

Para ejecutar las pruebas localmente:

```bash
python manage.py test
```

---

## Contacto

Para cualquier pregunta o inquietud, no dudes en contactarme.

*Desarrollado como parte de prueba técnica para posición de Desarrollador de Software*