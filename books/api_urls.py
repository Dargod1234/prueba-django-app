from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('libros/', api_views.LibroListCreateView.as_view(), name='libro-list-create'),
    path('libros/<int:pk>/', api_views.LibroDetailView.as_view(), name='libro-detail'),
    path('libros/<int:pk>/prestar/', api_views.prestar_libro, name='prestar-libro'),
    path('libros/<int:pk>/devolver/', api_views.devolver_libro, name='devolver-libro'),
]