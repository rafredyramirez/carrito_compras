from django.db import models

# Create your models here.
class Producto(models.Model):
    sku = models.CharField(max_length=50, blank=False, null=False)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.CharField(max_length=50, blank=False, null=False)
    cantidad_disponible = models.FloatField()
    precio_unitario = models.FloatField()

    class Meta:
        managed = True
        db_table = 'producto'

    def __str__(self):
        return self.nombre
