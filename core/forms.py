from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

# crear formulario nasheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

class ProductoForm(ModelForm):

    nombre = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=800,widget=forms.Textarea(attrs={"rows":4}))    
    
    class Meta:
        
        model = Producto
        #fields = ['nombre','precio','stock','descripcion','tipo']
        fields = '__all__'

        widgets = {
            'vencimiento' : forms.SelectDateWidget(years=range(1940,2024))
        }
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserEditForm(forms.ModelForm):
    donacion = forms.DecimalField(label='Donación', min_value=1000, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','donacion']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ('nombre', 'email', 'mensaje')


class CuponForm(forms.ModelForm):
    class Meta:
        model = Cupon
        fields = ['codigo', 'descuento', 'fecha_fin']
        widgets = {
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    