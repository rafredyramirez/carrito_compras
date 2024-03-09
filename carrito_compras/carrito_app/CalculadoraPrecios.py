class CalculadoraPrecios:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def _obtener_tipo_producto(self):
        if str(self.producto.sku).startswith('WE'):
            self.tipo_producto = 'peso'
        elif str(self.producto.sku).startswith('SP'):
            self.tipo_producto = 'descuento'
        else:
            self.tipo_producto = 'normal'

    def calcular_acumulado(self):
        self._obtener_tipo_producto()
        if self.tipo_producto == 'peso':
            acumulado = 1 * 1000 * self.producto.precio_unitario * self.cantidad
        elif self.tipo_producto == 'descuento':
            cociente = divmod(self.cantidad, 3)[0]
            if cociente == 1:
                descuento = 0.2
            elif cociente == 2:
                descuento = 0.4
            elif cociente >= 3:
                descuento = 0.5
            else:
                descuento = 0
            acumulado = (self.producto.precio_unitario * self.cantidad) - (self.producto.precio_unitario * self.cantidad * descuento)
        else:
            acumulado = self.producto.precio_unitario * self.cantidad
        return acumulado
