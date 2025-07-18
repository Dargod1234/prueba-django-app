from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.ListarLibrosView.as_view(), name='listar_libros'),
    path('libro/<int:pk>/', views.DetalleLibroView.as_view(), name='detalle_libro'),
    path('libro/crear/', views.CrearLibroView.as_view(), name='crear_libro'),
    path('libro/<int:pk>/editar/', views.EditarLibroView.as_view(), name='editar_libro'),
    path('libro/<int:pk>/prestar/', views.PrestarLibroView.as_view(), name='prestar_libro'),
    path('libro/<int:pk>/devolver/', views.DevolverLibroView.as_view(), name='devolver_libro'),
    path('mis-libros/', views.MisLibrosView.as_view(), name='mis_libros'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='books:listar_libros'), name='logout'),
]