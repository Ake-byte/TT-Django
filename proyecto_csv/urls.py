from unicodedata import name
from . import views
from django.urls import path

app_name = 'csv'

urlpatterns = [
    # Inicio - /csv/
    path('', views.index, name='index'),
    # Listado Registros - /csv/Registros
    path('ListadoRegistros', views.listadoRegistros, name='listadoRegistros'),
    # Ver registro High - /csv/id
    path('<int:id>/', views.detalleRegistro, name='detalleRegistro'),
    # Crear registro - /csv/form
    path('CrearRegistro', views.crearRegistro, name='crearRegistro'),
    # Editar registro
    path('editarRegistro/<int:id>/', views.editarRegistro, name="editarRegistro"),
]
