from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from .serializers import *
import requests


class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class TipoProductoViewset(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer    



# Create your views here.
def index(request):
    productoAll = Producto.objects.order_by('?')[:8]
    producto3 = Producto.objects.order_by('?')[:3]
    

    data = {
        'listado': productoAll,
        'listado3': producto3
        
    }
    
  

    return render(request, 'core/index.html', data)


def indexapi(request):
    #solicitud api --colocar las api de imagenes y ponerlo tambn en con data
    response = requests.get('http://127.0.0.1:8000/api/productos/')   
    response2 = requests.get('https://rickandmortyapi.com/api/character/')
    response3 = request.get('https://mindicador.cl/api/dolar')


    #productoAll = Producto.objects.order_by('?')[:8]
    #producto3 = Producto.objects.order_by('?')[:3]

    data = response.json()
    aux = response2.json()
    data3 = response3.json()

    #data3 = response.json()

    personajes = aux['results']

    data = {
        'listado': data,
        #'listado3': data3,
        'personajes': personajes
        
    }
    
  
    return render(request, 'core/indexapi.html', data)






def base(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    context = {
        'carrito': carrito,
    }
    return render(request, 'core/base.html', context)


def add(request):
    page = request.GET.get('page', 1)
    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid ():
            formulario.save()
            #data['msj'] = "Producto guardado correctamente" 
            messages.success(request, "Producto almacenado correctamente")  
    return render(request, 'core/add-product.html',data)

def update(request, id):
    producto = Producto.objects.get(id=id)
    data = {
        'form': ProductoForm(instance =producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, files=request.FILES,instance=producto)
        if formulario.is_valid():
            formulario.save()
            #data['msj'] = "Producto modificado correctamente"
            messages.success(request, "Producto modificado correctamente") 
            data['form'] = formulario
    
    return render(request, 'core/update.html', data)
def delate(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect(to = 'index')



def nosotros(request):
    return render(request, 'core/about.html')

@login_required
def carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    codigo_cupon = None
    total_general = 0
    sub_total = 0

    for item in carrito:
        total_producto = item.producto.precio * item.cantidad
        total_general += total_producto
        sub_total += total_producto
        item.total_individual = total_producto

    total_descuento = 0

    # Verificar si el usuario es suscriptor
    try:
        suscriptor = Suscriptor.objects.get(user=request.user)
        if suscriptor.es_suscriptor:
            descuento = suscriptor.descuento / 100
            total_descuento = round(total_general * descuento)
            total_general -= total_descuento
    except Suscriptor.DoesNotExist:
        # Manejar el caso cuando no se encuentra el objeto Suscriptor
        pass

    # Verificar si se ha enviado un cupón en el formulario
    if request.method == 'POST':
        codigo_cupon = request.POST.get('codigo_cupon')
        try:
            cupon = Cupon.objects.get(codigo=codigo_cupon)
            descuento_cupon = round(total_general * (cupon.descuento / 100))
            total_descuento += descuento_cupon
            total_general -= descuento_cupon
        except Cupon.DoesNotExist:
            # Manejar el caso cuando no se encuentra el cupón
            pass

    data = {
        'listado': carrito,
        'final_total': total_general,
        'sub_total': sub_total,
        'descuento': total_descuento,
        'codigo_cupon': codigo_cupon,
        
    }

    return render(request, 'core/cart.html', data)

@login_required
def agregar(request, id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        
        producto = Producto.objects.get(id=id)
        if producto.stock >= cantidad:
            carrito, created = Carrito.objects.get_or_create(producto=producto, usuario=request.user)

            if not created:
                carrito.cantidad += cantidad
            else:
                carrito.cantidad = cantidad
            carrito.save()

            # Mostrar el SweetAlert
            messages.success(request, 'Producto guardado')

    return redirect(request.META.get('HTTP_REFERER') or 'index')
@login_required
def eliminar (request, id):

    carrito = Carrito.objects.get(id=id)
    carrito.delete()
    return redirect('carrito')
@login_required
def actualizar(request, id):
    if request.method == 'POST':
        nueva_cantidad = request.POST.get('cantidad')
        item = Carrito.objects.get(id=id)
        item.cantidad = nueva_cantidad
        item.save()
        # Puedes agregar mensajes flash o redirigir a otra página después de la actualización
    return redirect('carrito')
@login_required
def pago(request, codigo_cupon=None):
    if request.method == 'POST':
        carrito = Carrito.objects.filter(usuario=request.user)

        for item in carrito:
            producto = item.producto
            cantidad_comprada = item.cantidad

            # Restar la cantidad comprada del stock del producto
            producto.stock -= cantidad_comprada
            producto.save()

            # Crear una instancia de Compra para el historial
            historial = Historial(
                usuario=request.user,
                producto=producto,
                cantidad=cantidad_comprada,
                total=item.producto.precio * cantidad_comprada,
                fecha=datetime.now()
            )
            historial.save()

        # Eliminar los productos del carrito
        carrito.delete()

        return redirect('carrito')

    carrito = Carrito.objects.filter(usuario=request.user)
    total_general = 0
    sub_total = 0

    for item in carrito:
        item.total = item.producto.precio * item.cantidad
        total_general += item.total
        sub_total += item.total

    # Aplicar descuento si el usuario es suscriptor
    total_descuento = 0
    try:
        suscriptor = get_object_or_404(Suscriptor, user=request.user)
        if suscriptor.es_suscriptor:
            descuento = suscriptor.descuento / 100
            total_descuento = round(total_general * descuento)
            total_general -= total_descuento
    except Suscriptor.DoesNotExist:
        # Manejar el caso cuando no se encuentra el objeto Suscriptor
        pass

    # Aplicar descuento del cupón
    if codigo_cupon:
        cupon = get_object_or_404(Cupon, codigo=codigo_cupon)
        descuento_cupon = round(total_general * (cupon.descuento / 100))
        total_descuento += descuento_cupon
        total_general -= descuento_cupon

    data = {
        'carrito': carrito,
        'total_general': total_general,
        'sub_total': sub_total,
        'descuento': total_descuento,
        'codigo_cupon': codigo_cupon
    }

    return render(request, 'core/checkout.html', data)

@login_required
def seguimiento(request):
    return render(request, 'core/seguimiento.html')

def detalle(request, id):
    producto = Producto.objects.get(id=id)
    productoAll = Producto.objects.order_by('?')[:8]
    
    data = {
        'producto': producto,
        'listado': productoAll,
    }
    
    return render(request, 'core/shop-detail.html',data)

def productos(request):

    productoAll = Producto.objects.all()
    tipos_producto = TipoProducto.objects.all()

    tipo_seleccionado = request.GET.get('tipo')  # Obtener el tipo seleccionado del formulario

    if tipo_seleccionado:
        productoAll = productoAll.filter(tipo__descripcion=tipo_seleccionado)

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productoAll, 6)
        productoAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productoAll,
        'paginator': paginator,
        'tipos_producto': tipos_producto,
        'tipo_seleccionado': tipo_seleccionado
    }

    
    return render(request, 'core/shop.html', data)
@login_required
def historial(request):
    compras = Historial.objects.filter(usuario=request.user)
    data = {
        'compras': compras
    }
    
    return render(request, 'core/wishlist.html',data)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardar el usuario registrado
            suscriptor = Suscriptor(user=user)  # Crear un objeto Suscriptor con el usuario
            suscriptor.save()  # Guardar el objeto Suscriptor en la base de datos
            return redirect('login')  # Redirige al inicio de sesión después del registro exitoso
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def edit(request):
    user = request.user
    suscriptor, created = Suscriptor.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
            donacion = request.POST.get('donacion')
            if donacion:
                total_donacion = float(donacion)
                if total_donacion >= 1000:
                    if not suscriptor.es_suscriptor:
                        suscriptor.es_suscriptor = True
                        suscriptor.descuento = 5
                        suscriptor.save()
                else:
                    form.add_error('donacion', 'La donación debe ser de al menos 1000')
            
            cancelar_suscripcion = request.POST.get('cancelar_suscripcion')
            if cancelar_suscripcion:
                cancelar_suscripcion(request, suscriptor) 
        
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'core/edit.html', {'form': form, 'suscriptor': suscriptor})

def eliminar_perfil(request):
    user = request.user
    user.delete()
    # Realiza cualquier otra acción necesaria después de eliminar el perfil
    return redirect('index') 

def cancelar_suscripcion(request):
    user = request.user
    suscriptor = Suscriptor.objects.get(user=user)
    suscriptor.es_suscriptor = False
    suscriptor.descuento = 0
    suscriptor.save()
    
    return redirect('edit') 


def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Realizar alguna acción adicional, como enviar un correo electrónico de notificación, etc.
            
            return redirect('contacto')  # Redirigir a la página de éxito o a donde desees
        else:
            messages.error(request, 'Hubo un error en el formulario.')
    else:
        form = ContactForm()
    return render(request, 'core/contact-us.html', {'form': form})


def crear_cupon(request):
    if request.method == 'POST':
        form = CuponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cupones')
    else:
        form = CuponForm()
    
    return render(request, 'core/crear_cupon.html', {'form': form})

def lista_cupones(request):
    cupones = Cupon.objects.all()
    return render(request, 'core/lista_cupones.html', {'cupones': cupones})

def actualizar_cupon(request, id):
    cupon = get_object_or_404(Cupon, id=id)
    
    if request.method == 'POST':
        form = CuponForm(request.POST, instance=cupon)
        if form.is_valid():
            form.save()
            return redirect('lista_cupones')
    else:
        form = CuponForm(instance=cupon)
    
    return render(request, 'core/actualizar_cupon.html', {'form': form})


def eliminar_cupon(request, id):
    cupon = get_object_or_404(Cupon, id=id)
    cupon.delete()
    return redirect('lista_cupones')