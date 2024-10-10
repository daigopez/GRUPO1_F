from django.urls import path
from . import views
from .views import (
    plato_list,
    plato_create,
    plato_update,
    plato_delete,
    
    pagina_venta,
    comprar_plato,
    editar_encuesta,
    visualizacion_encuestas,
    agregar_al_carrito,  
    restar_del_carrito,   
    eliminar_del_carrito, 
    lista_platos_semanales,
    crear_plato_semanal,
    editar_plato_semanal,
    eliminar_plato_semanal,
    votar_plato_semanal,
)

urlpatterns = [
    path('', views.iniciar_sesion, name='iniciar_sesion'),  # Ruta de inicio de sesión
    path('plato_list/', plato_list, name='plato_list'),  # Ruta para listar platos
    path('nuevo/', plato_create, name='plato_create'),  # Ruta para crear un nuevo plato
    path('editar/<int:pk>/', plato_update, name='plato_update'),  # Ruta para editar un plato
    path('eliminar/<int:pk>/', plato_delete, name='plato_delete'),  # Ruta para eliminar un plato
  
    path('venta/', pagina_venta, name='pagina_venta'),  # Ruta para la página de venta
    path('comprar/<int:plato_id>/', comprar_plato, name='comprar_plato'),  # Ruta para comprar un plato
    path('agregar/<int:plato_id>/', agregar_al_carrito, name='agregar_al_carrito'),  # Ruta para agregar al carrito
    path('restar/<int:plato_id>/', restar_del_carrito, name='restar_del_carrito'), # Ruta para restar del carrito
    path('eliminar-del-carrito/<int:plato_id>/', eliminar_del_carrito, name='eliminar_del_carrito'), # Ruta para eliminar del carrito
    path('editar_encuesta/<int:encuesta_id>/', editar_encuesta, name='editar_encuesta'),  # Ruta para editar encuestas
    path('visualizar-encuestas/', visualizacion_encuestas, name='visualizar_encuestas'),  # Ruta para visualizar encuestas

    # Rutas para platos semanales
    path('platos/semanales/', lista_platos_semanales, name='lista_platos_semanales'),
    path('platos/semanales/nuevo/', crear_plato_semanal, name='crear_plato_semanal'),
    path('platos/semanales/editar/<int:pk>/', editar_plato_semanal, name='editar_plato_semanal'),
    path('platos/semanales/eliminar/<int:pk>/', eliminar_plato_semanal, name='eliminar_plato_semanal'),
    path('platos/semanales/votar/<int:plato_semanal_id>/', votar_plato_semanal, name='votar_plato_semanal'),
]