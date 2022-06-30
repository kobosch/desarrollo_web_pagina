from django.urls import path
from  .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',index, name='index'),
    path ('carro', carro, name='carro'),
    path ('agregarProducto', agregarProducto, name='agregarProducto'),
    path ('adminProducto', adminProducto, name='adminProducto'),
    path ('eliminarProducto', eliminarProducto, name='eliminarProducto'),
    path ('modificarProducto', modificarProducto, name='modificarProducto'),
    path ('registro', agregarCliente, name='agregarCliente'),
    path ('login', login, name='login'),
    path ('productos', productos, name='productos'),
    path ('categorias', categorias, name='categorias'),
    path ('listaProductos', listProductos, name='listProductos'),
    path ('logout', logout, name='logout'),
    path ('adminUsuario', adminUsuario, name='adminUsuario'),
    path ('modificarUsuario', modificarUsuario, name='modificarUsuario'),
    path ('agregarUsuario', agregarUsuario, name='agregarUsuario'),
    path ('agregarTipoProducto', agregarTipoProducto, name='agregarTipoProducto'),
    path ('adminMenu', adminMenu, name='adminMenu'),
    path ('carrito', carrito, name='carrito'),
    path ('agregarCarro', agregarCarro, name='agregarCarro'),
    path ('ofertas', listOfertas, name='ofertas'),
    path ('ciudad', ciudad, name='ciudad'),
    path ('comprar', comprar, name='comprar'),
    path ('suscribirse', suscribirse, name='suscribirse'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
