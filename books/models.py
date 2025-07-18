from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = [
        ('regular', 'Usuario Regular'),
        ('admin', 'Administrador'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='regular')
    
    def get_rol_display(self):
        return dict(self.ROLES).get(self.rol, self.rol)
    
    def __str__(self):
        return self.username

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano_publicacion = models.IntegerField() 
    stock = models.IntegerField(default=0)
    usuarios_prestamo = models.ManyToManyField(Usuario, through='Prestamo', blank=True)
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        pass 