from django.urls import path
from . import views
from .views import (
    plato_list,
    plato_create,
    plato_update,
    plato_delete,
    logueo,
    pagina_venta,
    comprar_plato,
    editar_encuesta,
    visualizacion_encuestas,
    agregar_al_carrito,  
    restar_del_carrito,   
    eliminar_del_carrito, 
)

urlpatterns = [
    path('', views.iniciar_sesion, name='iniciar_sesion'),
    path('plato_list/', plato_list, name='plato_list'),  # Ruta principal para listar platos
    path('nuevo/', plato_create, name='plato_create'),  # Ruta para crear un nuevo plato
    path('editar/<int:pk>/', plato_update, name='plato_update'),  # Ruta para editar un plato
    path('eliminar/<int:pk>/', plato_delete, name='plato_delete'),  # Ruta para eliminar un plato
    path('logueo/', logueo, name='logueo'),  # Ruta para el logueo
    path('venta/', pagina_venta, name='pagina_venta'),  # Ruta para la página de venta
    path('comprar/<int:plato_id>/', comprar_plato, name='comprar_plato'),  # Ruta para comprar un plato
    path('agregar/<int:plato_id>/', agregar_al_carrito, name='agregar_al_carrito'),  # Ruta para agregar al carrito
    path('restar/<int:plato_id>/', restar_del_carrito, name='restar_del_carrito'), # Ruta para restar del carrito
    path('eliminar-del-carrito/<int:plato_id>/', eliminar_del_carrito, name='eliminar_del_carrito'), # Ruta para eliminar del carrito
    path('editar_encuesta/<int:encuesta_id>/', editar_encuesta, name='editar_encuesta'),  # Ruta para editar encuestas
    path('visualizar-encuestas/', visualizacion_encuestas, name='visualizar_encuestas'),  # Ruta para visualizar encuestas
]