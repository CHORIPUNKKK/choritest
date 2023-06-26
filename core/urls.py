from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('productos', ProductoViewset)
router.register('tipo_productos', TipoProductoViewset)
<<<<<<< HEAD
router.register('Cupon', CuponViewset)
router.register('User', UserViewset)

=======
>>>>>>> main


urlpatterns = [
    path('', index, name='index'),
    path('indexapi/', indexapi, name='indexapi'),
    path('contacto/', contacto, name='contacto'),
    path('carrito/', carrito, name='carrito'),
    path('pago/', pago, name='pago'),
    path('pago/<str:codigo_cupon>/', pago, name='pago_con_cupon'),
    path('seguimiento/', seguimiento, name='seguimiento'),
    path('detalle/<id>', detalle, name='detalle'),
    path('productos/', productos, name='productos'),
    path('add/', add, name='add'),
    path('update/<id>/', update, name='update'),
    path('delate/<id>/', delate, name='delate'),
    path('agregar/<id>/', agregar, name='agregar'),
    path('eliminar/<id>/', eliminar, name='eliminar'),
    path('actualizar/<id>/', actualizar, name='actualizar'),
    path('accounts/register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('historial/', historial, name='historial'),
    path('cancelar-suscripcion/', cancelar_suscripcion, name='cancelar_suscripcion'),
    path('eliminar-perfil/', eliminar_perfil, name='eliminar_perfil'),
    path('crear/', crear_cupon, name='crear_cupon'),
    path('listar/', lista_cupones, name='lista_cupones'),
    path('actualizar_cup/<id>/', actualizar_cupon, name='actualizar_cupon'),
    path('elimina_cup/<id>/', eliminar_cupon, name='eliminar_cupon'), 
    path('api/', include(router.urls)),

]