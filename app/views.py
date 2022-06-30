from django.shortcuts import render, redirect
from .models import Carrito, Productos, Usuario, TipoUsuario, TipoProducto
from django.contrib import messages
import requests
import json
from random import randint
from django.http import HttpResponse

def WebService(Path, Params, Method="GET", files=None):
    # url de la api

    url = "http://127.0.0.1:8000/" + Path
    # obtener la respuesta de la api enviando la url y los parametros
    if(Method == "GET"):
        response = requests.get(url, params=Params)
    elif(Method == "POST"):
        response = requests.post(url, data=Params, files=files)
    elif(Method == "PUT"):
        response = requests.put(url, data=Params, files=files)
    elif(Method == "DELETE"):
        response = requests.delete(url, data=Params)

    if(response.status_code == 200):
        # convertir la respuesta a json
        data = json.loads(response.text)
        # retornar la respuesta
        return data
    else:
        print("Error")
        print(response.text)
        return False


# crear decorador para validar si el usuario esta logueado
def validarUsuario(request):
    if 'usuario' in request.session:
        return True
    else:
        return False


def productos(request):
    return render(request, 'app/productos.html', {'productos': productos})


def categorias(request):
    # obtener todas los tipos de productos
    tipos = WebService('tipo_producto', {})
    return render(request, 'app/categorias.html', {'tipos': tipos})


def validarUsuarioAdmin(request):
    if 'usuario' in request.session:
        print(request.session['usuario'])
        if request.session["usuario"]["TipoUsuario"].lower() == "administrador":
            return True
        else:
            return False
    else:
        return False

# get Productos


def GetProductos():
    productos = Productos.objects.all()
    return productos

# obtener producto por su id


def getProducto(id):
    producto = Productos.objects.get(IdProducto=id)
    return producto


def listProductos(request):
    if request.method == 'GET':
        if "categoria" in request.GET:
            categoria = request.GET['categoria']
            productos = WebService('producto', {'tipo': categoria})
            print(productos)
            cagegorianombre = request.GET['category']
            return render(request, 'app/ListProductos.html', {'productos': productos, "categoria": categoria, "cagegorianombre": cagegorianombre})
        productos = Productos.objects.all().order_by('IdProducto')
        return render(request, 'app/ListProductos.html', {'productos': productos})


def listOfertas(request):
    if request.method == 'GET':
        productos = WebService('producto', {'inOferta': True})
        print(productos)
        return render(request, 'app/ListProductos.html', {'productos': productos,  "cagegorianombre": "Ofertas"})


def agregarProducto(request):
    # si el metodo es post recibe los parametros para agregar un producto
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    # si no existen categorias crear una

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        cantidad = request.POST['cantidad']
        # obtener imagen desde el formulario
        tipo = request.POST['tipo']
        imagen = request.FILES['imagen']
        oferta = request.POST['oferta']
        # guardr imagen en el servidor y obtener el nombre de la imagen
        nombreImagen = imagen.name
        # guardar la imagen en el servidor
        with open('media/' + nombreImagen, 'wb+') as destination:
            for chunk in imagen.chunks():
                destination.write(chunk)

        # generar nombre randon

        nombreRandon = nombre.replace(" ", "")
        nombreRandon = nombreRandon.lower()
        nombreRandon = nombreRandon + str(randint(1, 100))+".png"
        # crear el producto
        files = [
            ('imagen', (nombreRandon, open(
                'media/' + nombreImagen, 'rb'), 'image/png'))
        ]
        if oferta == '':
            oferta = 0
        producto = WebService('producto', {'nombre': nombre, 'descripcion': descripcion,
                              'precio': precio, 'stock': cantidad, 'tipo': tipo, 'oferta': oferta}, "POST", files)
        return redirect('/categorias')
    elif request.method == 'GET':
        Categorias = WebService('tipo_producto', {})
        return render(request, 'app/agregarProducto.html', {'categorias': Categorias})


def modificarProducto(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    if request.method == 'GET':
        id = request.GET['id']
        producto = WebService('producto', {'id': id})
        print(producto)
        Categorias = WebService('tipo_producto', {})
        print(Categorias)
        return render(request, 'app/agregarProducto.html', {'Producto': producto, "categorias": Categorias})
    elif request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        cantidad = request.POST['cantidad']
        id = int(request.POST['IdProducto'])
        tipo = request.POST['tipo']
        oferta = request.POST['oferta']
        imagen = None
        print("files")
        print(request.FILES)
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
        payload = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'stock': cantidad,
            'tipo': tipo,
            'id': id,
            'oferta': oferta
        }
        files = None
        if imagen is not None:
            nombreImagen = imagen.name
            # guardar la imagen en el servidor
            with open('media/' + nombreImagen, 'wb+') as destination:
                for chunk in imagen.chunks():
                    destination.write(chunk)
            # generar nombre randon
            nombreRandon = nombre.replace(" ", "")
            nombreRandon = nombreRandon.lower()
            nombreRandon = nombreRandon + str(randint(1, 100))+".png"
            files = [
                ('imagen', (nombreRandon, open(
                    'media/' + nombreImagen, 'rb'), 'image/png'))
            ]
            print("files")
            print("==============================")
            print(files)
            print("==============================")
        producto = WebService('producto', payload, "PUT", files)
        messages.success(request, 'Producto Modificado correctamente!')
        return redirect('adminProducto')


def eliminarProducto(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    id = request.GET['id']
    Productos.objects.filter(IdProducto=id).delete()
    messages.success(request, 'Producto eliminado correctamente!')

    return redirect('adminProducto')

    # redireccionar a la pagina de adminProducto

def comprar(request):
    if validarUsuario(request) == False:
        return redirect('/')
    if request.method == 'POST':
        direccion = request.POST['direccion']
        ciudad = request.POST['ciudad']
        tarjeta = request.POST['tarjeta']
        usuario =  request.session['usuario']["Id"]
        payload = {
            'direccion': direccion,
            'Ciudad': ciudad,
            'Tarjeta': tarjeta,
            'idUsuario': usuario
        }
        print(payload)
        venta = WebService('venta', payload, "POST")
        idVenta= venta["idVenta"]
        print(idVenta)
        print("=============Venta===============")
        print(venta)
        print("=============Venta===============")
        for producto in request.session['carro']:
            payload = {
                'idVenta': idVenta,
                'idProducto': producto['id'],
                'cantidad': producto['cantidad']
            }
            ventaProducto = WebService('detalle_venta', payload, "POST")
            print(ventaProducto)

        request.session['carro'] = []
        messages.success(request, 'Compra realizada correctamente!')
        return redirect('carrito')

  

def adminProducto(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    print(request.session['usuario'])
    productos = WebService('producto', {})
    return render(request, 'app/adminProducto.html', {'productos': productos})

# Create your views here.


def index(request):
    # insertar ("test", "producto de prueba", 20, 21)
    productos = GetProductos()
    for x in productos:
        print(x.Nombre)
    return render(request, 'app/index.html')


def carro(request):
    return render(request, 'app/carro.html')

  
# agregar usuario
def agregarCliente(request):
    if request.method == 'POST':
        print("entra aqui")
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        tipo = 2
        # validar que el usuario no exista
        payload = {
            'nombre': nombre,
            'apellido': apellido,
            'email': correo,
            'password': contrasena,
            'tipo_usuario': tipo
        }
        usuario = WebService('usuario', payload, "POST")
        messages.success(request, 'Usuario agregado correctamente!')
        return redirect('/')

        return render(request, 'app/registro.html',)
    elif request.method == 'GET':
        return render(request, 'app/registro.html')

def suscribirse(request):
    if request.method == 'POST':
        idUsuario = request.session['usuario']['Id']
        payload = {
            "id": idUsuario,
            "suscribe":True
        }
        usuario = WebService('usuario', payload, "PUT")
        Usuario = request.session['usuario']
        Usuario['suscrito'] = True
        request.session['usuario'] = Usuario
        messages.success(request, 'Suscripcion realizada correctamente!')
        return redirect('categorias')

def login(request):
    if request.method == 'POST':
        correo = request.POST['email']
        contrasena = request.POST['password']
        usuario = WebService('usuario', {
                             'email': correo, 'password': contrasena, "login": True}, Method='POST')
        if(usuario == False):
            return render(request, 'app/index.html', {'mensaje': 'Usuario o contraseña incorrectos'})
        if (usuario is not None):
            print("==========================")
            print(usuario)
            print("==========================")
            # convertir usuario en diccionario
            User = {
                "Id": usuario["id"],
                'Nombre': usuario["nombre"],
                'Apellido': usuario["apellido"],
                'Correo': usuario["email"],
                'TipoUsuario': usuario["tipo_usuario"],
                'id_tipo': usuario["id_tipo"],
                'suscrito': usuario["suscrito"]
            }
            request.session['usuario'] = User
            carro = []
            request.session['carro'] = carro
            # redireccionar a la pagina de adminProducto
            return redirect('categorias')
        else:
            return render(request, 'app/index.html', {'mensaje': 'Usuario o contraseña incorrectos'})
    elif request.method == 'GET':
        if "usuario" in request.session:
            return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


# listar usuarios existentes
def adminUsuario(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    usuarios = WebService('usuario', {})
    return render(request, 'app/adminUsuario.html', {'usuarios': usuarios})

# eliminar usuario


# modificar usuario


def modificarUsuario(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    if request.method == 'POST':
        id = request.POST['id']
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        tipo = request.POST['tipo']
        apellido = request.POST['apellido']

        payload = {
            'id': id,
            'nombre': nombre,
            'apellido': apellido,
            'email': correo,
            'tipo_usuario': tipo,
        }
        usuario = WebService('usuario', payload, "PUT")
        messages.success(request, 'Usuario Modificado correctamente!')
        return redirect('adminUsuario')
    else:
        id = request.GET['id']
        usuario = WebService('usuario', {'id': id})
        tipos = WebService('tipo_usuario', {})
        return render(request, 'app/registroAdmin.html', {'usuario': usuario, 'tipos': tipos})

# agregar usuario


def agregarUsuario(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    if request.method == 'POST':
        # obtener tipo de usuario
        tipo = request.POST['tipo']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        payload = {
            'nombre': nombre,
            'apellido': apellido,
            'email': correo,
            'password': contrasena,
            'tipo_usuario': tipo,
            'suscrito': False
        }
        usuario = WebService('usuario', payload, Method='POST')
        if(usuario == False):
            return render(request, 'app/adminUsuario.html', {'mensaje': 'El usuario ya existe'})
        if (usuario != False):
            messages.success(request, 'Usuario guardado correctamente!')
            return redirect('adminUsuario')
        else:
            return render(request, 'app/adminUsuario.html', {'mensaje': 'Error al guardar usuario'})

    else:
        tipos = WebService('tipo_usuario', {})
        return render(request, 'app/registroAdmin.html', {'tipos': tipos})

# agregar tipo de producto


def agregarTipoProducto(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        WebService('tipo_producto', {
            'nombre': nombre, 'descripcion': descripcion}, Method='POST')
        messages.success(request, 'Tipo de producto guardado correctamente!')
        return redirect('agregarTipoProducto')
        # agregar tipo de producto
        # redireccionar a la pagina de adminProducto
        return redirect('adminProducto')
    else:
        return render(request, 'app/tipoProducto.html')


def adminMenu(request):
    if validarUsuarioAdmin(request) == False:
        return redirect('/')
    return render(request, 'app/adminMenu.html')


# metodo de agregar al carro
def agregarCarro(request):
    if validarUsuario(request) == False:
        return redirect('/')
    if request.method == 'POST':
        id = request.POST['id']
        cantidad = request.POST['cantidad']
        producto = WebService('producto', {'id': id})
        print("==========================")
        print(producto)
        print("==========================")
        carro = request.session['carro']
        found = False
        for x in carro:
            if "id" in x:
                if x['id'] == id:
                    precio = str(x["precio"])
                    # elimninar numeros despues de la coma en el precio
                    precio = precio.split('.')
                    precio = precio[0]
                    x['cantidad'] = int(x['cantidad']) + int(cantidad)
                    x['total'] = int(precio)*int(x['cantidad'])
                    found = True
                    break

        if found is False:
            if request.session['usuario']['suscrito'] == True and int(producto['precioOferta']) > 0:
                precio = str(producto["precioOferta"])
            else:
                precio = str(producto['precio'])
            # elimninar numeros despues de la coma en el precio
            precio = precio.split('.')
            precio = precio[0]

            if request.session['usuario']['suscrito'] == True and producto["precioOferta"] > 0:

                carro.append({
                    'id': id,
                    'nombre': producto["nombre"],
                    'precio': producto["precioOferta"],
                    'cantidad': cantidad,
                    'total': int(precio)*int(cantidad)
                })
            else:
                carro.append({
                    'id': id,
                    'nombre': producto["nombre"],
                    'precio': producto["precio"],
                    'cantidad': cantidad,
                    'total': int(precio)*int(cantidad)
                })

        request.session['carro'] = carro
        return redirect('carrito')

# carrito de compra

def ciudad(request):
    idPais = request.GET['idPais']
    ciudad = WebService('ciudad', {"idPais":idPais})
    #transformar ciudad a json
    ciudad = json.dumps(ciudad)
    return HttpResponse(ciudad, content_type='application/json')

def carrito(request):
    if validarUsuario(request) == False:
        return redirect('/')
    carro = request.session['carro']
    total = 0
    for x in carro:
        if "total" in x:
            total += x['total']
    Pais = WebService('pais', {})

    print(Pais)
    return render(request, 'app/carro.html', {'carro': carro, 'total': total, 'Pais': Pais})
