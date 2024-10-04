from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Plato, Encuesta
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
    carrito = request.session.get('carrito', {})
    platos_carrito = []
    total = 0

    # Procesar cada plato en el carrito
    for plato_id, cantidad in carrito.items():
        plato = get_object_or_404(Plato, id=plato_id)
        subtotal = plato.precio * cantidad
        total += subtotal
        platos_carrito.append({
            'plato': plato,
            'cantidad': cantidad,
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
    carrito = request.session.get('carrito', {})
    carrito[plato_id] = carrito.get(plato_id, 0) + 1  # Aumentar cantidad o inicializar a 1
    request.session['carrito'] = carrito
    return redirect('pagina_venta')

def restar_del_carrito(request, plato_id):
    carrito = request.session.get('carrito', {})
    if plato_id in carrito:
        if carrito[plato_id] > 1:
            carrito[plato_id] -= 1
        else:
            del carrito[plato_id]
    request.session['carrito'] = carrito
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
        return redirect('plato_list')
    return render(request, 'comercio/plato_confirm_delete.html', {'plato': plato})