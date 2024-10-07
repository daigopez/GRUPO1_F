from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Plato, Encuesta, Carrito, ItemCarrito
from .forms import PlatoForm, EncuestaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

# Verificación de usuario administrador
def es_administrador(user):
    return user.is_staff

def index(request):
    return render(request, 'index.html')

def logueo(request):
    return render(request, 'logueo.html')

def registro(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('iniciada')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm(),
                    "error": 'El usuario ya existe.'
                })
        return render(request, 'registro.html', {
            'form': UserCreationForm(),
            "error": 'Las contraseñas no coinciden.'
        })
    return render(request, 'registro.html', {'form': UserCreationForm()})

@login_required
def iniciada(request):
    return render(request, 'iniciada.html')

def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))

def iniciar_sesion(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario o contraseña incorrectos.'
            })
        login(request, user)
        return redirect('iniciada')
    return render(request, 'iniciar.html', {'form': AuthenticationForm()})

def lista_de_platos(request):
    platos = Plato.objects.all()
    return render(request, 'comercio/lista_de_platos.html', {'platos': platos})

def pagina_venta(request):
    platos = Plato.objects.all()
    total = 0
    platos_carrito = []

# Obtener los platos del carrito desde la base de datos
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(user=request.user)

        items = ItemCarrito.objects.filter(carrito=carrito)
        for item in items:
            subtotal = item.plato.precio * item.cantidad
            total += subtotal
            platos_carrito.append({
                'plato': item.plato,
                'cantidad': item.cantidad,
                'subtotal': subtotal,
            })

# Manejo de encuestas
    form = EncuestaForm()
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.plato = get_object_or_404(Plato, id=request.POST['plato_id'])
            encuesta.save()
            messages.success(request, '¡Gracias por tu encuesta!')
            return redirect('pagina_venta')

    return render(request, 'comercio/pagina_venta.html', {
        'platos': platos,
        'platos_carrito': platos_carrito,
        'total': total,
        'form': form
    })

def agregar_al_carrito(request, plato_id):
    if request.user.is_authenticated:
        plato = get_object_or_404(Plato, id=plato_id)
        
        # Obtener o crear el carrito para el usuario
        carrito, created = Carrito.objects.get_or_create(user=request.user)

        # Manejar el item del carrito
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, plato=plato)

        if not created:
            item.cantidad += 1  # Incrementar cantidad si ya existe
        item.save()  # Guardar en la base de datos


    else:
        messages.error(request, 'Debes iniciar sesión para agregar platos al carrito.')
    
    return redirect('pagina_venta')

def restar_del_carrito(request, plato_id):
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, user=request.user)
        item = get_object_or_404(ItemCarrito, carrito=carrito, plato_id=plato_id)

        if item.cantidad > 1:
            item.cantidad -= 1
  
        else:
            item.delete()
    
        item.save()
    return redirect('pagina_venta')

def eliminar_del_carrito(request, plato_id):
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, user=request.user)
        item = get_object_or_404(ItemCarrito, carrito=carrito, plato_id=plato_id)
        item.delete()

    return redirect('pagina_venta')

def editar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    
    if request.method == "POST":
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta actualizada con éxito.')
            return redirect('pagina_venta')
    else:
        form = EncuestaForm(instance=encuesta)

    return render(request, 'comercio/encuesta_form.html', {'form': form})

def visualizacion_encuestas(request):
    platos = Plato.objects.all()
    resultados = []

    for plato in platos:
        encuestas = plato.encuestas.all()
        total_rating = sum(encuesta.rating for encuesta in encuestas) if encuestas.exists() else 0
        cantidad_encuestas = encuestas.count()
        promedio_rating = total_rating / cantidad_encuestas if cantidad_encuestas > 0 else 0

        resultados.append({
            'plato': plato,
            'total_rating': total_rating,
            'promedio_rating': promedio_rating,
            'cantidad_encuestas': cantidad_encuestas,
        })

    resultados.sort(key=lambda x: x['promedio_rating'], reverse=True)

    return render(request, 'visualizacion_encuestas.html', {'resultados': resultados})

def comprar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    messages.success(request, f'Has comprado {plato.nombre} por ${plato.precio}.')
    return redirect('pagina_venta')

@login_required
@permission_required('is_superuser')
def plato_list(request):
    platos = Plato.objects.all()
    return render(request, 'comercio/plato_list.html', {'platos': platos})

@user_passes_test(es_administrador)
@login_required
def plato_create(request):
    if request.method == "POST":
        form = PlatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato creado con éxito.')
            return redirect('plato_list')
    else:
        form = PlatoForm()
    return render(request, 'comercio/plato_form.html', {'form': form})

@login_required
@permission_required('is_superuser')
def plato_update(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato actualizado con éxito.')
            return redirect('plato_list')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'comercio/plato_form.html', {'form': form})

@login_required
@permission_required('is_superuser')
def plato_delete(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        plato.delete()
        messages.success(request, 'Plato eliminado con éxito.')
        return redirect('plato_list')
    return render(request, 'comercio/plato_confirm_delete.html', {'plato': plato})