from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Marcas"


class Producto(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    unidades = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(limit_value=1)])
    vip = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.marca}{self.modelo}'

    class Meta:
        unique_together = ['marca', 'modelo']
        verbose_name_plural = "Productos"


class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)
    vip = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name_plural = "Clientes"


class Compra(models.Model):
    user = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.PositiveIntegerField()
    importe = models.DecimalField(decimal_places=2, max_digits=7)
    iva = models.DecimalField(decimal_places=2, max_digits=3)

    def __str__(self):
        return f'{self.user}{self.producto}'

    class Meta:
        unique_together = ['user', 'fecha']
