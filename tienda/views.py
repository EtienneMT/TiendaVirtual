from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction
from .models import Producto, Cliente, Marca, Compra
from .form import FormProducto, FormCompra, FormBuscarProducto, FormSingIn, FormLogIn
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def welcome(request):
    productos = Producto.objects.all()
    form = FormBuscarProducto(request.GET)

    if form.is_valid():
        texto_busqueda = form.cleaned_data['texto']
        marcas_seleccionadas = form.cleaned_data['marca']
        if len(marcas_seleccionadas) != 0:
            productos_filtrados = productos.filter(marca_id__in=marcas_seleccionadas)
        else:
            productos_filtrados = productos
        productos_filtrados = productos_filtrados.filter(nombre__contains=texto_busqueda)
        return render(request, 'tienda/index.html', {'productos': productos_filtrados, 'form': form})

    return render(request, 'tienda/index.html', {'productos': productos, 'form': form})


@login_required(login_url='/tienda/login/')
@staff_member_required
def listado_producto(request):
    producto = Producto.objects.all()
    return render(request, 'tienda/admin/listado.html', {'productos': producto})


@login_required(login_url='/tienda/login/')
@staff_member_required
def nuevo_producto(request):
    if request.method == "POST":
        form = FormProducto(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('producto_admin')
    else:
        form = FormProducto()
    return render(request, 'tienda/admin/producto.html', {'form': form})


@login_required(login_url='/tienda/login/')
@staff_member_required
def edit_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = FormProducto(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('producto_admin')
    else:
        form = FormProducto(instance=producto)
    return render(request, 'tienda/admin/producto.html', {'form': form})


@login_required(login_url='/tienda/login/')
@staff_member_required
def admin_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('producto_admin')


@transaction.atomic
@login_required(login_url='/tienda/login/')
def checkout(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    cliente = get_object_or_404(Cliente, user=request.user)
    if request.method == "POST":
        form = FormCompra(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.user = cliente
            compra.producto = producto
            compra.fecha = timezone.now()
            compra.iva = 0.21
            compra.unidades = form.cleaned_data['unidades']
            compra.importe = compra.unidades * producto.precio
            producto.unidades = producto.unidades - compra.unidades
            cliente.saldo = cliente.saldo - compra.importe
            cliente.save()
            producto.save()
            compra.save()
            return redirect('welcome')
    form = FormCompra()
    return render(request, 'tienda/checkout.html', {'form': form, 'producto': producto})


@login_required(login_url='/tienda/login/')
@staff_member_required
def informe_marca(request):
    marcas = Marca.objects.all()
    producto = Producto.objects.all()
    return render(request, 'tienda/marcas.html', {'marcas': marcas, 'productos': producto})


def sing_in(request):
    if request.method == 'POST':
        form = FormSingIn(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            cliente = Cliente(user=user, saldo=0, vip=False)
            cliente.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = FormSingIn()

    return render(request, 'tienda/login.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
    form = FormLogIn(request.POST)
    return render(request, 'tienda/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('welcome')


@login_required(login_url='/tienda/login/')
@staff_member_required
def top_productos(request):
    top_producto = Producto.objects.annotate(purchase_count=Count('compra')).order_by('-purchase_count')[:10]
    return render(request, 'tienda/top_productos.html', {'top_productos': top_producto})


@login_required(login_url='/tienda/login/')
def historial_compras(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    compras = Compra.objects.all().filter(producto__compra__user_id=cliente)
    return render(request, 'tienda/historial.html', {'compras': compras})


@login_required(login_url='/tienda/login/')
@staff_member_required
def top_clientes(request):
    top_cliente = Cliente.objects.annotate(dinero_gastado=Sum('compra__importe')).order_by('-dinero_gastado')[:10]
    return render(request, 'tienda/top_clientes.html', {'top_clientes': top_cliente})
