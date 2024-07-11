from django.db import models

class MarcaRepuesto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'marcarepuesto'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return self.nombre

class MarcaMoto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'marcamoto'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return self.nombre

class UnidadMedida(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'unidadmedida'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return self.descripcion

class Pais(models.Model):
    fabricacion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'pais'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return self.fabricacion

class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    marca_moto = models.ForeignKey(MarcaMoto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'modelo'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    nro = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)

    class Meta:
        db_table = 'proveedor'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    codigo = models.IntegerField(unique=True)
    numero_parte = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_lista = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    marca_repuesto = models.ForeignKey(MarcaRepuesto, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    modelos = models.ManyToManyField(Modelo, through='RepuestoModelo')
    foto_url = models.URLField(max_length=200, blank=True, null=True)  # Campo de foto URL

    class Meta:
        db_table = 'repuesto'  # Nombre de la tabla en minúsculas

    def __str__(self):
        return f"{self.nombre} ({self.numero_parte})"

class RepuestoModelo(models.Model):
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'repuestomodelo'  # Nombre de la tabla en minúsculas
        unique_together = ('repuesto', 'modelo')

class RepuestoProxy(Repuesto):
    class Meta:
        proxy = True
        verbose_name = 'Repuesto Simple'
        verbose_name_plural = 'Repuestos Simples'
