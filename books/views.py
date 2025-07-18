from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Libro, Prestamo, Usuario
from .forms import LibroForm
from django.contrib.auth.views import LoginView as DjangoLoginView

class ListarLibrosView(ListView):
    """
    Vista para listar todos los libros disponibles en la biblioteca (stock > 0).
    """
    model = Libro
    template_name = 'books/listar_libros.html'
    context_object_name = 'libros'
    
    def get_queryset(self):
        """
        Devuelve solo los libros que tienen stock disponible.
        """
        return Libro.objects.filter(stock__gt=0)

class DetalleLibroView(DetailView):
    """
    Vista para mostrar los detalles de un libro específico.
    """
    model = Libro
    template_name = 'books/detalle_libro.html'
    context_object_name = 'libro'

class EsAdminMixin(UserPassesTestMixin):
    """
    Mixin para restringir el acceso a vistas solo a usuarios con rol de 'admin'.
    """
    def test_func(self) -> bool:
        """
        Verifica si el usuario autenticado tiene el rol de 'admin'.
        """
        return self.request.user.is_authenticated and self.request.user.rol == 'admin'

class CrearLibroView(LoginRequiredMixin, EsAdminMixin, CreateView):
    """
    Vista para crear un nuevo libro.
    Requiere que el usuario esté autenticado y tenga el rol de 'admin'.
    """
    model = Libro
    template_name = 'books/crear_libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('books:listar_libros')

class EditarLibroView(LoginRequiredMixin, EsAdminMixin, UpdateView):
    """
    Vista para editar un libro existente.
    Requiere que el usuario esté autenticado y tenga el rol de 'admin'.
    """
    model = Libro
    template_name = 'books/editar_libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('books:listar_libros')

class PrestarLibroView(LoginRequiredMixin, View):
    """
    Vista para que un usuario regular pueda prestar un libro.
    """
    def post(self, request, pk: int):
        """
        Maneja la solicitud POST para prestar un libro.
        Verifica el rol del usuario, el stock del libro y si el usuario ya tiene el libro prestado.
        """
        if request.user.rol != 'regular':
            messages.error(request, 'Solo usuarios regulares pueden prestar libros.')
            return redirect('books:detalle_libro', pk=pk)
        
        libro = get_object_or_404(Libro, pk=pk)
        
        # Verificar si el usuario ya tiene este libro prestado activamente
        prestamo_activo = Prestamo.objects.filter(
            usuario=request.user, 
            libro=libro, 
            activo=True
        ).exists()
        
        if prestamo_activo:
            messages.error(request, 'Ya tienes este libro prestado. Por favor, devuélvelo antes de intentar prestarlo de nuevo.')
            return redirect('books:detalle_libro', pk=pk)
        
        if libro.stock > 0:
            Prestamo.objects.create(usuario=request.user, libro=libro, activo=True)
            libro.stock -= 1
            libro.save()
            messages.success(request, f'Has prestado "{libro.titulo}" exitosamente.')
        else:
            messages.error(request, 'No hay stock disponible para este libro.')
        
        return redirect('books:detalle_libro', pk=pk)

class MisLibrosView(LoginRequiredMixin, ListView):
    """
    Vista para listar todos los libros que el usuario actual ha prestado o devuelto.
    Requiere que el usuario esté autenticado.
    """
    template_name = 'books/mis_libros.html'
    context_object_name = 'prestamos'
    
    def get_queryset(self):
        """
        Devuelve todos los registros de préstamo (activos e inactivos)
        asociados al usuario autenticado, ordenados por fecha de préstamo descendente.
        """
        return Prestamo.objects.filter(usuario=self.request.user).order_by('-fecha_prestamo')
    
class LoginView(DjangoLoginView):
    """
    Vista personalizada para el inicio de sesión de usuarios.
    """
    template_name = 'books/login.html'
    
    def get_success_url(self) -> str:
        """
        Define la URL a la que se redirige después de un inicio de sesión exitoso.
        """
        return reverse_lazy('books:listar_libros')
    
class DevolverLibroView(LoginRequiredMixin, View):
    """
    Vista para que un usuario regular pueda devolver un libro.
    """
    def post(self, request, pk: int):
        """
        Maneja la solicitud POST para devolver un libro.
        Verifica el rol del usuario y si el libro está actualmente prestado por él.
        """
        if request.user.rol != 'regular':
            messages.error(request, 'Solo usuarios regulares pueden devolver libros.')
            return redirect('books:mis_libros')
        
        libro = get_object_or_404(Libro, pk=pk)
        
        try:
            # Busca el préstamo ACTIVO que el usuario tiene para este libro
            prestamo = Prestamo.objects.get(
                usuario=request.user, 
                libro=libro, 
                activo=True
            )
            
            prestamo.fecha_devolucion = timezone.now()
            prestamo.activo = False # Marca el préstamo como inactivo
            prestamo.save()
            
            libro.stock += 1
            libro.save()
            
            messages.success(request, f'Has devuelto "{libro.titulo}" exitosamente.')
        except Prestamo.DoesNotExist:
            # Si no se encuentra un préstamo activo, el libro no está prestado o ya ha sido devuelto.
            messages.info(request, 'Este libro no está prestado por ti o ya ha sido devuelto.')
        except Exception as e:
            # Captura cualquier otro error inesperado durante el proceso de devolución.
            messages.error(request, f'Ocurrió un error inesperado al intentar devolver el libro: {e}')
        
        return redirect('books:mis_libros')
