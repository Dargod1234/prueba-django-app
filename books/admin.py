from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Libro, Prestamo

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'rol', 'is_staff']
    list_filter = ['rol', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'ano_publicacion', 'stock']  # Cambiar aquí
    list_filter = ['ano_publicacion', 'autor']  # Cambiar aquí
    search_fields = ['titulo', 'autor']

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'activo']
    list_filter = ['activo', 'fecha_prestamo']
    search_fields = ['usuario__username', 'libro__titulo']