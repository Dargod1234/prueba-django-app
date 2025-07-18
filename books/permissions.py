from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir:
    - Lectura (GET, HEAD, OPTIONS) a cualquier usuario (autenticado o no).
    - Escritura (POST, PUT, PATCH, DELETE) solo a usuarios autenticados con rol 'admin'.
    """
    def has_permission(self, request, view) -> bool:
        """
        Verifica si el usuario tiene permiso para realizar la acción solicitada.
        """
        # Permite métodos seguros (lectura) a cualquier usuario.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para otros métodos (escritura), requiere que el usuario sea un administrador autenticado.
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

class IsRegularUser(permissions.BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios autenticados con rol 'regular'.
    """
    def has_permission(self, request, view) -> bool:
        """
        Verifica si el usuario tiene permiso para realizar la acción solicitada.
        """
        # Requiere que el usuario esté autenticado y tenga el rol 'regular'.
        return request.user and request.user.is_authenticated and request.user.rol == 'regular'
