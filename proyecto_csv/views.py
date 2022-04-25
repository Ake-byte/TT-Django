from multiprocessing import context
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm
from .models import Registro
from .utils import preprocesar, graficar, get_graficas, regresion, arbolDesicionRegresion

import pandas as pd
# Create your views here.

@login_required(login_url="/login")
def index(request):
    
    return render(request, 'csv/index.html')

@login_required(login_url="/login")
def listadoRegistros(request):
    lista_registro = Registro.objects.all()
    context = {
        'lista_registro': lista_registro,
    }

    if request.method == "POST":
        registro_id = request.POST.get("csv-id")
        registro = Registro.objects.filter(id=registro_id).first()
        if registro and registro.user == request.user:
            registro.delete()

    return render(request, 'csv/ListadoRegistros.html', context)

@login_required(login_url="/login")
def detalleRegistro(request, id):
    registro = Registro.objects.get(pk=id)
    graficas = get_graficas(id)
    df = pd.read_csv(registro.archivo_registro)
    regresion(df)
    arbolDesicionRegresion(df)
    context = {
        'registro': registro,
        'graficas': graficas,
    }
    return render(request, 'csv/DetalleRegistro.html', context)

@login_required(login_url="/login")
def crearRegistro(request):
    form = RegistroForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        archivo = pd.read_csv(instance.archivo_registro)
        content = preprocesar(archivo).to_csv()
        temp_file = ContentFile(content.encode('utf-8'))
        instance.archivo_registro.save(f'{instance.archivo_registro}', temp_file)
        archivo = pd.read_csv(instance.archivo_registro)
        graficar(instance.id, archivo)
        instance.user = request.user
        instance.save()
        return redirect('csv:index')

    return render(request, 'csv/RegistroForm.html', {'form': form})

@login_required(login_url="/login")
def editarRegistro(request, id):
    registro = Registro.objects.get(id=id)
    form = RegistroForm(request.POST or None, instance=registro)

    if form.is_valid():
        form.save()
        return redirect('csv:index')

    return render(request, 'csv/RegistroForm.html', {'form': form, 'registro': registro})

#@login_required(login_url="/login")
#def eliminarRegistro(request, id):

#    registro = Registro.objects.get(id=id)

#    if request.method == 'POST':
#        registro.delete()
#        return redirect('csv:index')

#    return render(request, 'csv/RegistroDelete.html', {'registro': registro})
