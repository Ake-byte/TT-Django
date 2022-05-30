from multiprocessing import context
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from usuarios.models import PermisoUsuario
=======
import chardet
import io
import csv
>>>>>>> 08f63d7a3b7825adf6ba74e2d74ee4623e21e4df

from .forms import PrediccionRegresionForm, RegistroForm, PrediccionArbolForm
from .models import Registro
from .utils import *

import pandas as pd
# Create your views here.

@login_required(login_url="/login")
def index(request):
    
    return render(request, 'csv/index.html')

@login_required(login_url="/login")
def listadoRegistros(request):
    if request.user.is_superuser:
        lista_registro = Registro.objects.all
    else :    
        lista_registro = Registro.objects.filter(user=request.user)
    context = {
        'lista_registro': lista_registro,
    }

    if request.method == "POST":
        registro_id = request.POST.get("csv-id")
        registro = Registro.objects.filter(id=registro_id).first()
        if registro and registro.user == request.user or request.user.is_superuser:
            registro.delete()

    return render(request, 'csv/ListadoRegistros.html', context)

@login_required(login_url="/login")
def detalleRegistro(request, id):
    registro = Registro.objects.get(pk=id)
<<<<<<< HEAD
    usuario = request.user
    permisoUsuario = PermisoUsuario.objects.get(user=usuario)
    df = pd.read_csv(registro.archivo_registro)
=======
    df = registro.archivo_registro.read().decode('ISO-8859-1')
    df = pd.read_csv(io.StringIO(df))
>>>>>>> 08f63d7a3b7825adf6ba74e2d74ee4623e21e4df
    rs1 = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5)
    rs2 = df.groupby('Order Date')['Quantity'].sum().sort_values(ascending=False).head(5)
    rs3 = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5)
    rs4 = df.groupby('Order Date')['Sales'].sum().sort_values(ascending=False).head(5)
    rs_pie = df.groupby("Category")["Quantity"].agg("sum")
    rs_pie2 = df.groupby("Sub-Category")["Quantity"].agg("sum")
    categories1 = list(rs1.index)
    values1 = list(rs1.values)
    categories2 = list(rs2.index)
    values2 = list(rs2.values)
    categories3 = list(rs3.index)
    values3 = list(rs3.values)
    categories4 = list(rs4.index)
    values4 = list(rs4.values)

    copia = df.copy(deep=True)
    precision, regresion_entrenado = ModeloRegresion(copia)
    copia = df.copy(deep=True)
    precision_arbol, arbol_entrenado = modeloArbolDesicionClasificacion(copia)
    day = month = sales = 0
    prediccionArbol = prediccionRegresion = ''
    product_name = quantityR = dayR = monthR = 0
    if request.method == "POST":
        form = PrediccionArbolForm(request.POST)
        formR = PrediccionRegresionForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data["day"]
            month = form.cleaned_data["month"]
            sales = form.cleaned_data["sales"]
            quantity = form.cleaned_data["quantity"]
            prediccionArbol = arbolDesicionClasificacion(arbol_entrenado, day, month, sales, quantity)
        if formR.is_valid():
            product_name = formR.cleaned_data["product_name"]
            quantityR = formR.cleaned_data["quantity"]
            dayR = formR.cleaned_data["day"]
            monthR = formR.cleaned_data["month"]
            prediccionRegresion = regresion(regresion_entrenado, product_name, quantityR, dayR, monthR)
    else:
        form = PrediccionArbolForm()
        formR = PrediccionRegresionForm()
    copia = df.copy(deep=True)
    asociacion = reglasAsociacion(id, copia)
    grafo = get_reglas(id)

    data = []
    for index in range(0, len(rs_pie.index)):
        # print(rs_pie.index[index])
        value = {'name': rs_pie.index[index], 'y': rs_pie.values[index]  }
        data.append(value)
	
    data2 = []
    for index in range(0, len(rs_pie2.index)):
        # print(rs_pie.index[index])
        value = {'name': rs_pie2.index[index], 'y': rs_pie2.values[index]  }
        data2.append(value)

    context = {"categories1": categories1, 'values1': values1, 
    "categories2": categories2, 'values2': values2, 
    "categories3": categories3, 'values3': values3, 
    "categories4": categories4, 'values4': values4, 
    'data': data,
    'data2': data2,
    'registro': registro,
    'precision': precision,
    'precision_arbol': precision_arbol,
    'asociacion': asociacion,
    'grafo': grafo,
<<<<<<< HEAD
    'permisoUsuario': permisoUsuario,
    'prediccionArbol': prediccionArbol
=======
    'form': form,
    'prediccionArbol': prediccionArbol,
    'prediccionRegresion': prediccionRegresion,
    'formR': formR
>>>>>>> 08f63d7a3b7825adf6ba74e2d74ee4623e21e4df
    }
    return render(request, 'csv/DetalleRegistro2.html', context=context)

@login_required(login_url="/login")
def crearRegistro(request):
    form = RegistroForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        #enc = chardet.detect(instance.archivo_registro.read())
        #print(enc)
        archivo = instance.archivo_registro.read().decode('ISO-8859-1')
        archivo = pd.read_csv(io.StringIO(archivo))
        content = preprocesar(archivo).to_csv()
        temp_file = ContentFile(content.encode('ISO-8859-1'))
        instance.archivo_registro.save(f'{instance.archivo_registro}', temp_file)
<<<<<<< HEAD
        archivo = pd.read_csv(instance.archivo_registro)
        #graficar(instance.id, archivo)
=======
        archivo = instance.archivo_registro.read().decode('ISO-8859-1')
        archivo = pd.read_csv(io.StringIO(archivo))
>>>>>>> 08f63d7a3b7825adf6ba74e2d74ee4623e21e4df
        instance.user = request.user
        instance.save()
        return redirect('csv:index')

    return render(request, 'csv/RegistroForm.html', {'form': form})

@login_required(login_url="/login")
def editarRegistro(request, id):
    registro = Registro.objects.get(id=id)
    form = RegistroForm(request.POST or None, request.FILES or None, instance=registro)

    if form.is_valid():
        instance = form.save(commit=False)
        #enc = chardet.detect(instance.archivo_registro.read())
        #print(enc)
        archivo = instance.archivo_registro.read().decode('ISO-8859-1')
        archivo = pd.read_csv(io.StringIO(archivo))
        content = preprocesar(archivo).to_csv()
        temp_file = ContentFile(content.encode('ISO-8859-1'))
        instance.archivo_registro.save(f'{instance.archivo_registro}', temp_file)
        archivo = instance.archivo_registro.read().decode('ISO-8859-1')
        archivo = pd.read_csv(io.StringIO(archivo))
        instance.user = request.user
        instance.save()
        return redirect('csv:index')

    return render(request, 'csv/RegistroForm.html', {'form': form, 'registro': registro})