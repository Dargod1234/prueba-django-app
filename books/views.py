from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Libro, Prestamo, Usuario
from .forms import LibroForm # <--- Nueva importación
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import authenticate, login

class ListarLibrosView(ListView):
    model = Libro
    template_name = 'books/listar_libros.html'
    context_object_name = 'libros'
    
    def get_queryset(self):
        return Libro.objects.filter(stock__gt=0)

class DetalleLibroView(DetailView):
    model = Libro
    template_name = 'books/detalle_libro.html'
    context_object_name = 'libro'

class EsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'admin'

class CrearLibroView(LoginRequiredMixin, EsAdminMixin, CreateView):
    model = Libro
    template_name = 'books/crear_libro.html'
    form_class = LibroForm # <--- Usamos el formulario personalizado
    success_url = reverse_lazy('books:listar_libros')

class EditarLibroView(LoginRequiredMixin, EsAdminMixin, UpdateView):
    model = Libro
    template_name = 'books/editar_libro.html'
    form_class = LibroForm # <--- Usamos el formulario personalizado
    success_url = reverse_lazy('books:listar_libros')

class PrestarLibroView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.rol != 'regular':
            messages.error(request, 'Solo usuarios regulares pueden prestar libros.')
            return redirect('books:detalle_libro', pk=pk)
        
        libro = get_object_or_404(Libro, pk=pk)
        
        # Verificar si ya tiene el libro prestado activamente
        prestamo_activo = Prestamo.objects.filter(
            usuario=request.user, 
            libro=libro, 
            activo=True
        ).exists()
        
        if prestamo_activo:
            messages.error(request, 'Ya tienes este libro prestado. Por favor, devuélvelo antes de intentar prestarlo de nuevo.')
            return redirect('books:detalle_libro', pk=pk)
        
        if libro.stock > 0:
            Prestamo.objects.create(usuario=request.user, libro=libro, activo=True) # Aseguramos activo=True al crear
            libro.stock -= 1
            libro.save()
            messages.success(request, f'Has prestado "{libro.titulo}" exitosamente.')
        else:
            messages.error(request, 'No hay stock disponible para este libro.')
        
        return redirect('books:detalle_libro', pk=pk)

class MisLibrosView(LoginRequiredMixin, ListView):
    template_name = 'books/mis_libros.html'
    context_object_name = 'prestamos'
    
    def get_queryset(self):
        # Muestra todos los préstamos del usuario, ordenados por la fecha de préstamo más reciente
        return Prestamo.objects.filter(usuario=self.request.user).order_by('-fecha_prestamo')
    
class LoginView(DjangoLoginView):
    template_name = 'books/login.html'
    
    def get_success_url(self):
        return reverse_lazy('books:listar_libros')
    
class DevolverLibroView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user.rol != 'regular':
            messages.error(request, 'Solo usuarios regulares pueden devolver libros.')
            return redirect('books:mis_libros')
        
        libro = get_object_or_404(Libro, pk=pk)
        
        try:
            prestamo = Prestamo.objects.get(
                usuario=request.user, 
                libro=libro, 
                activo=True
            )
            
            prestamo.fecha_devolucion = timezone.now()
            prestamo.activo = False
            prestamo.save()
            
            libro.stock += 1
            libro.save()
            
            messages.success(request, f'Has devuelto "{libro.titulo}" exitosamente.')
        except Prestamo.DoesNotExist:
            messages.info(request, 'Este libro no está prestado por ti o ya ha sido devuelto.') # Mensaje más informativo
        except Exception as e: # Captura cualquier otro error inesperado
            messages.error(request, f'Ocurrió un error inesperado al intentar devolver el libro: {e}')
        
        return redirect('books:mis_libros')