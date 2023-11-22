from django import forms
from .models import Producto, Compra, Marca
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

MARCAS_ENTRADAS = [
    ('Sony', 'Sony'),
    ('Samsung', 'Samsung'),
    ('Apple', 'Apple'),
    ('Logitech', 'Logitech'),
    ('LG', 'LG'),
    ('Corsair', 'Corsair'),
    ('Xiaomi', 'Xiaomi'),
    ('Razer', 'Razer')
]


class FormProducto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['marca', 'nombre', 'modelo', 'unidades', 'precio', 'vip']


class FormCompra(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['unidades']


class FormBuscarProducto(forms.Form):
    texto = forms.CharField(required=False, widget=forms.TextInput({"placeholder": "Search ..."}))
    marca = forms.ModelMultipleChoiceField(required=False, queryset=Marca.objects.all(), widget=forms.CheckboxSelectMultiple)


class FormSingIn(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FormLogIn(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']
