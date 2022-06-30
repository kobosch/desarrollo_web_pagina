from django.contrib import admin

# Register your models here.
from .models import Productos, Usuario, TipoUsuario, TipoProducto
#mostrar modelos en el administrative site

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["Nombre" , "Descripcion" , "Precio", "Cantidad", "IdTipoProducto"]
    list_editable = ["Precio"]
    ordering = ["Cantidad"]
    search_fields=["Nombre","Precio","Cantidad"]
    list_filter=["Nombre", "Precio"]
    list_per_page= 5
 

admin.site.register(Productos, ProductoAdmin)
admin.site.register(Usuario)
admin.site.register(TipoUsuario)
admin.site.register(TipoProducto)
