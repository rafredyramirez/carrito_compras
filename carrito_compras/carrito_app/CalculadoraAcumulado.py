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
            acumulado = ((1000 * self.producto.precio_unitario) * self.cantidad)
        
        # Si es de descuento especial, primero se obtiene el descuento a aplicar
        # por cada grupo de descuento hasta un máximo de 0.5
        elif self.tipo_producto == 'descuento':
            descuento_maximo = 0.5  # Descuento máximo del 50%
            descuento_por_unidades = 0.2  # Descuento del 20% por cada grupo de unidades
            cantidad_unidades_descuento=3 # Cantidad de unidades para el descuento

            # Calcular cuántos grupos de cantidad de unidades para descuento hay en la cantidad total
            grupos_de_tres = self.cantidad // cantidad_unidades_descuento

            # Se obtiene la cantidad de grupos de 3 que realmente van a tener descuento
            cantidad_grupos_exacto=0
            porcentajeAnterior=0
            porcentajeTem=0
            for _ in range(grupos_de_tres):               
                porcentajeTem=porcentajeTem+descuento_por_unidades
                if porcentajeTem<=descuento_maximo:
                    cantidad_grupos_exacto+=1
                else:
                    if porcentajeAnterior<=descuento_maximo and porcentajeTem>descuento_maximo:
                        cantidad_grupos_exacto+=1
                    porcentajeTem=round(porcentajeTem+descuento_por_unidades, 2) 
                porcentajeAnterior=porcentajeTem

            # Calcular el precio con descuento por grupos de unidades a las que les aplica
            precio_con_descuento = 0    
            porcentaje_aplicado=descuento_por_unidades        
            porcentaje_aplicado_real=0    
            for _ in range(grupos_de_tres):
                if porcentaje_aplicado<=descuento_maximo and porcentaje_aplicado_real<=descuento_maximo:
                    precio_con_descuento += self.producto.precio_unitario * cantidad_unidades_descuento * (1 - descuento_por_unidades)
                    porcentaje_aplicado =porcentaje_aplicado + descuento_por_unidades
                    porcentaje_aplicado_real=round(porcentaje_aplicado_real + descuento_por_unidades,2)
                elif porcentaje_aplicado_real <= descuento_maximo:
                    precio_con_descuento += self.producto.precio_unitario * cantidad_unidades_descuento * (1 - round(descuento_maximo - porcentaje_aplicado_real,2))
                    porcentaje_aplicado_real=round(porcentaje_aplicado_real + descuento_por_unidades,2)

            # Calcular el precio sin descuento para las unidades restantes
            unidades_restantes = self.cantidad % cantidad_unidades_descuento
            # Se valida si las variables tiene el mismo valor o no
            if grupos_de_tres==cantidad_grupos_exacto:
                # son iguales se calcula con el descuento que se trae
                precio_con_descuento += self.producto.precio_unitario * unidades_restantes
            else:
                # son diferentes se calcula la cantidad de unidades restantes
                unidades_restantes = self.cantidad - cantidad_grupos_exacto*cantidad_unidades_descuento
                precio_con_descuento += self.producto.precio_unitario * unidades_restantes

            # Calcular el precio sin descuento
            precio_sin_descuento = self.producto.precio_unitario * self.cantidad
            
            # Calcular el precio total con el descuento acumulado
            acumulado = min(precio_con_descuento, precio_sin_descuento)

        # Para un producto normal simplmente se multiplica el precio por la cantidad
        else:
            acumulado = self.producto.precio_unitario * self.cantidad
        return acumulado
