from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los administradores crear, actualizar o eliminar.
    Permite la lectura a todos (incluidos no autenticados).
    """
    def has_permission(self, request, view):
        # Permite GET, HEAD, OPTIONS a cualquier usuario (autenticado o no)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo permite otros métodos (POST, PUT, PATCH, DELETE) si el usuario es un administrador autenticado
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

class IsRegularUser(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a usuarios regulares autenticados.
    """
    def has_permission(self, request, view):
        # Solo permite si el usuario está autenticado y tiene el rol 'regular'
        return request.user and request.user.is_authenticated and request.user.rol == 'regular'