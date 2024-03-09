from carrito_app.CalculadoraAcumulado import CalculadoraAcumulado

class Carrito:
    def __init__(self, request):
        # Obtener la referencia a la variable (dict) de la sesion actual
        self.session = request.session
        # Sino existe la entrada carrito, se crea en la sesion
        if not self.session.get('carrito'):
            self.session['carrito'] = {}
            self.carrito = self.session['carrito']
        else:
            # Si existe el carrito en la sesion, se obtiene en una variable a parte
            self.carrito = self.session.get('carrito')

    def guardar_carrito(self):
        # Actualizar el carrito en la sesion
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def agregar(self, producto):
        id = str(producto.id)
        if (id not in self.carrito.keys()) and (producto.cantidad_disponible > 0):
            self.carrito[id]={
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'acumulado': CalculadoraAcumulado(producto, 1).calcular_acumulado(),
                'cantidad': 1,
            }
            respuesta = True
        elif (id in self.carrito.keys()) and (self.carrito[id]['cantidad'] + 1 <= producto.cantidad_disponible):
            self.carrito[id]['cantidad'] += 1
            self.carrito[id]['acumulado'] = CalculadoraAcumulado(producto, self.carrito[id]['cantidad']).calcular_acumulado()
            respuesta = True
        else:
            respuesta = False
        self.guardar_carrito()
        return respuesta

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]['cantidad'] -= 1
            self.carrito[id]['acumulado'] = CalculadoraAcumulado(producto, self.carrito[id]['cantidad']).calcular_acumulado()
            if self.carrito[id]['cantidad'] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True