from django.shortcuts import render, redirect
from carrito_app.Carrito import Carrito
from carrito_app.models import Producto, Venta
from django.contrib import messages

# Create your views here.
def tienda(request):
    productos = Producto.objects.all()
    ventas_tienda = Venta.objects.all()
    venta_total_tienda = sum([venta.valor_total for venta in ventas_tienda])
    return render(
        request, 'tienda.html', 
        {
            'productos': productos,
            'ventas': venta_total_tienda,
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

def finalizar_compra(request):
    compra_finalizar = Carrito(request)
    if len(compra_finalizar.carrito) == 0:
        messages.error(request, 'Agrega al menos un producto al carrito')
        return redirect('tienda')
    else:
        valor_total_venta = 0
        for id, producto_carrito in compra_finalizar.carrito.items():
            valor_total_venta = valor_total_venta  + producto_carrito['acumulado']
            producto_bd = Producto.objects.get(id=id)
            producto_bd.cantidad_disponible = producto_bd.cantidad_disponible - producto_carrito['cantidad']
            producto_bd.save()
        Venta.objects.create(valor_total=valor_total_venta)
        compra_finalizar.limpiar()
        messages.success(request, 'Compra finalizada exitosamente')
        return redirect('tienda')