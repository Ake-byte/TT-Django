from django import forms
from .models import Registro


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['nombre_registro', 'descripcion_registro', 'archivo_registro']

class PrediccionArbolForm(forms.Form):
    day = forms.IntegerField()
    month = forms.IntegerField()
    sales = forms.FloatField()