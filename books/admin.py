from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Libro, Prestamo

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del panel de administración para el modelo Usuario.
    Personaliza la visualización y edición de usuarios en el admin de Django.
    """
    list_display = ['username', 'email', 'rol', 'is_staff']
    list_filter = ['rol', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Libro.
    Define cómo se muestran y se pueden buscar los libros en el admin.
    """
    list_display = ['titulo', 'autor', 'ano_publicacion', 'stock']
    list_filter = ['ano_publicacion', 'autor']
    search_fields = ['titulo', 'autor']

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Prestamo.
    Permite visualizar y filtrar los registros de préstamos de libros.
    """
    list_display = ['usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'activo']
    list_filter = ['activo', 'fecha_prestamo']
    search_fields = ['usuario__username', 'libro__titulo']
