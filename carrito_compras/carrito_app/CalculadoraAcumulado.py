class CalculadoraAcumulado:
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
        # Obtener el tipo de producto para saber la regla de calculo del acumulado
        self._obtener_tipo_producto()

        # Calcular acumulado segun el tipo de producto
        # Si es de peso, se toma el precio por gramo, multiplicado por 1000
        # para convertirlo a precio por kilo que es la unidad de venta
        if self.tipo_producto == 'peso':
            acumulado = 1000 * self.producto.precio_unitario * self.cantidad
        # Si es de descuento especial, primero se obtiene el descuento a aplicar
        # y luego se calcula el valor total con descuento
        elif self.tipo_producto == 'descuento':
            cociente = divmod(self.cantidad, 3)[0] # Cociente de dividir entre 3
            if cociente == 1:
                descuento = 0.2
            elif cociente == 2:
                descuento = 0.4
            elif cociente >= 3:
                descuento = 0.5
            else:
                descuento = 0
            acumulado = (self.producto.precio_unitario * self.cantidad) * (1 - descuento)
        # Para un producto normal simplmente se multiplica el precio por la cantidad
        else:
            acumulado = self.producto.precio_unitario * self.cantidad
        return acumulado
