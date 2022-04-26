import imp
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth import get_user_model
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Bienvenido {username}, has iniciado sesión exitosamente.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'usuarios/Registro.html', {'form': form})


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