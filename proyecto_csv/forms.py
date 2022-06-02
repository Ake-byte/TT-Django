from django import forms
from .models import Registro
from django.core.validators import MaxValueValidator, MinValueValidator 

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['nombre_registro', 'descripcion_registro', 'archivo_registro']

class PrediccionArbolForm(forms.Form):
    day = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    month = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

class PrediccionRegresionForm(forms.Form):
    product_name = forms.CharField()
    quantity = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    day = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    month = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])