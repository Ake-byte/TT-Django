from unicodedata import name
from . import views
from django.urls import path

app_name = 'usuarios'

urlpatterns = [
    path('verUsuario/<int:id>/', views.verUsuario, name='verUsuario'),
]