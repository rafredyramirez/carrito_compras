from django.shortcuts import render, redirect
from carrito_app.Carrito import Carrito
from carrito_app.models import Producto
from django.contrib import messages

# Create your views here.
def tienda(request):
    productos = Producto.objects.all()
    return render(
        request, 'tienda.html', 
        {
            'productos': productos, 
            'carrito': request.session['carrito'] if 'carrito' in request.session.keys() else {}
        }
    )

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    respuesta = carrito.agregar(producto)
    if not respuesta:
        messages.error(request, 'Se ha excedido la cantidad de producto disponible')
    return redirect('tienda')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('tienda')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('tienda')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('tienda')