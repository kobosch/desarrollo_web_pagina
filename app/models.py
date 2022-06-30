from django.db import models
from django.core.files.storage import FileSystemStorage


#modelo de tipo de usuario
class TipoUsuario(models.Model):
    IdTipoUsuario = models.AutoField(primary_key=True,auto_created=True)
    Nombre = models.CharField(max_length=30)
    Descripcion = models.CharField(max_length=30)
    class Meta:
        db_table = 'TipoUsuario'
    def __str__(self):
        return self.Nombre

#tipo producto product
class TipoProducto(models.Model):
    IdTipoProducto = models.AutoField(primary_key=True,auto_created=True)
    Nombre = models.CharField(max_length=30)
    Descripcion = models.CharField(max_length=30)

    class Meta:
        db_table = 'TipoProducto'

    def __str__(self):
        return self.Nombre

class Productos(models.Model):
    IdProducto = models.AutoField(primary_key=True,auto_created=True)
    Nombre = models.CharField(max_length=30)
    Descripcion = models.CharField(max_length=30)
    Precio = models.IntegerField()
    Cantidad = models.IntegerField()
    IdTipoProducto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    Imagen = models.ImageField(upload_to='img/products/')

    class Meta:
        db_table = 'Productos'

    
    def __str__(self):
        return self.Nombre
  


#modelo de usuario
class Usuario(models.Model):
    IdUsuario = models.AutoField(primary_key=True,auto_created=True)
    Nombre = models.CharField(max_length=500)
    Correo = models.CharField(max_length=30)
    Contrasena = models.CharField(max_length=30)
    IdTipoUsuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre
    class Meta:
        db_table = 'Usuario'

    

class Carrito(models.Model):
    Nombre = models.CharField(max_length=30)
    Precio = models.IntegerField()

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'Carrito'

    


