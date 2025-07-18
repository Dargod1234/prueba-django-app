from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser de Django.
    Incluye un campo 'rol' para diferenciar entre usuarios regulares y administradores.
    """
    ROLES = [
        ('regular', 'Usuario Regular'),
        ('admin', 'Administrador'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='regular')
    
    def get_rol_display(self) -> str:
        """
        Devuelve la representación legible del rol del usuario.
        """
        return dict(self.ROLES).get(self.rol, self.rol)
    
    def __str__(self) -> str:
        """
        Representación en cadena del objeto Usuario.
        """
        return self.username

class Libro(models.Model):
    """
    Modelo para representar un libro en la biblioteca.
    """
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano_publicacion = models.IntegerField() 
    stock = models.IntegerField(default=0)
    # Relación muchos a muchos con Usuario a través del modelo Prestamo
    usuarios_prestamo = models.ManyToManyField(Usuario, through='Prestamo', blank=True)
    
    def __str__(self) -> str:
        """
        Representación en cadena del objeto Libro.
        """
        return self.titulo

class Prestamo(models.Model):
    """
    Modelo para registrar un préstamo de un libro por un usuario.
    Permite un historial completo de préstamos y devoluciones.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True) # Indica si el préstamo está actualmente activo o el libro ha sido devuelto
    
    class Meta:
        # No se define unique_together para permitir múltiples registros de préstamo
        # para el mismo usuario y libro a lo largo del tiempo, facilitando el historial.
        pass
