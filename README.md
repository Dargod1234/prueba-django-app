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
git clone [URL_DEL_REPOSITORIO]
cd nombre-del-directorio-de-tu-proyecto