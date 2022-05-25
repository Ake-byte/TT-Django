import imp
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, PermisoUsuarioForm
#from django.contrib.auth.models import User
from .models import User, PermisoUsuario
from django.contrib.auth import get_user_model
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        formPermiso = PermisoUsuarioForm(request.POST)
        if form.is_valid() and formPermiso.is_valid():
            usuario = form.save()

            permiso = formPermiso.save(commit=False)
            #permiso.tipoPermiso = 1
            permiso.user = usuario
            permiso.save()

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Bienvenido {username}, has iniciado sesión exitosamente.')
            return redirect('login')
    else:
        form = RegisterForm()
        tipoPermiso = {'tipoPermiso':1}
        formPermiso = PermisoUsuarioForm(data=tipoPermiso)

    context = {'form': form,
    'formPermiso': formPermiso,}
    return render(request, 'usuarios/Registro.html', context)


@login_required
def profilePage(request):
    return render(request, 'usuarios/Perfil.html')

@login_required(login_url="/login")
def listadoUsuarios(request):
    if request.user.is_superuser:
        User = get_user_model()
        users = User.objects.all()
        context = {
            'lista_usuario': users,
        }

        return render(request, 'usuarios/ListadoUsuarios.html', context)
    
    messages.error(
    request, f'Lo sentimos {request.user.username}, no tienes permisos para acceder a este recurso.')
    return redirect('csv:index')

@login_required(login_url="/login")
def verUsuario(request, id):
    if request.user.is_superuser:
        usuario = User.objects.get(pk=id)
        permisoUsuario = PermisoUsuario.objects.get(user=usuario)

        context = {
            'usuario': usuario,
            'permisoUsuario': permisoUsuario,
        }
        print(usuario.username)
        print(usuario.id)
        return render(request, 'usuarios/VerUsuario.html', context)
    
    messages.error(
    request, f'Lo sentimos {request.user.username}, no tienes permisos para acceder a este recurso.')
    return redirect('csv:index')

@login_required(login_url="/login")
def editarUsuario(request, id):
    usuario = User.objects.get(pk=id)
    permisoUsuario = PermisoUsuario.objects.get(user=usuario)
    form = PermisoUsuarioForm(request.POST or None, instance=permisoUsuario)

    if form.is_valid():
        form.save()
        return redirect('csv:index')

    context = {
        'usuario': usuario,
        'form': form,
    }

    return render(request, 'usuarios/EditarUsuario.html', context)