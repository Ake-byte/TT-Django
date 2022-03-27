import imp
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Bienvenido {username}, tu cuenta ha sido creada.')
            return redirect('csv:index')
    else:
        form = RegisterForm()
    return render(request, 'usuarios/Registro.html', {'form': form})
