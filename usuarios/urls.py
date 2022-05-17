from unicodedata import name
from . import views
from django.urls import path

app_name = 'usuarios'

urlpatterns = [
    #Ver Usuario
    path('verUsuario/<int:id>/', views.verUsuario, name='verUsuario'),
    # Editar Usuario
    path('editarUsuario/<int:id>/', views.editarUsuario, name="editarUsuario"),
]