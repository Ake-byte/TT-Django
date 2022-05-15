"""tt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from re import template
from django import views
from django.contrib import admin
from django.urls import include, path
from usuarios import views as user_views
from django.contrib.auth import views as authentication_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csv/', include('proyecto_csv.urls')),
    path('registro/', user_views.register, name="register"),
    path('login/', authentication_views.LoginView.as_view(
        template_name='usuarios/Login.html'), name='login'),
    path('logout/', authentication_views.LogoutView.as_view(
        template_name='usuarios/Login.html'), name='logout'),
    path('PerfilUsuario/', user_views.profilePage, name='profile'),
    path('usuarios/', include('usuarios.urls')),
    path('ListadoUsuarios/', user_views.listadoUsuarios, name='listadoUsuarios'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)