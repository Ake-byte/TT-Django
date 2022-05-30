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
        if form.is_valid():
            usuario = form.save()
            tipoPermiso = {'tipoPermiso':1}
            formPermiso = PermisoUsuarioForm(data=tipoPermiso)
            permiso = formPermiso.save(commit=False)
            permiso.user = usuario
            permiso.save()

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Bienvenido {username}, has iniciado sesión exitosamente.')
            return redirect('csv:index')
    else:
        form = RegisterForm()
        
        

    context = {'form': form,
    }
    return render(request, 'usuarios/Registro.html', context)


@login_required
def profilePage(request):
    permisoUsuario = PermisoUsuario.objects.get(user=request.user)
    context = {
            'permisoUsuario': permisoUsuario,
        }

    return render(request, 'usuarios/Perfil.html', context)

@login_required(login_url="/login")
def listadoUsuarios(request):
    if request.user.is_superuser:
        User = get_user_model()
        users = User.objects.all()
        context = {
            'lista_usuario': users,
        }

        if request.method == "POST":
            usuario_id = request.POST.get("usuario-id")
            User = get_user_model()
            usuario = User.objects.get(pk=usuario_id)
            usuario.delete()

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