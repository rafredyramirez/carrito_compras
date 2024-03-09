class CalculadoraPrecios:
    def __init__(self, producto):
        self.producto = producto

    def _obtener_tipo_producto(self):
        lista_tipos = ['EA', 'WE', 'SP']



        if str(self.producto.sku).startswith('WE'):
            self.tipo_producto = 'peso'
        elif str(self.producto.sku).startswith('SP'):
            self.tipo_producto = 'descuento'
        else:
            self.tipo_producto = 'normal'

    def calcular_precio(self):
        self._obtener_tipo_producto()

        if self.tipo_producto == 'peso':
            precio = 1 * 1000 * self.producto.precio_unitario
        elif self.tipo_producto == 'descuento':
            precio = ''
        else:
            precio = self.producto.precio_unitario
        return precio
