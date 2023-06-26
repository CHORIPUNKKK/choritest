from django.contrib import admin
from .models import *
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo','created_at', 'updated_at']
    search_fields = ['nombre']
    list_per_page = 8   
    list_filter= ['tipo']
    list_editable =  ['precio','stock','descripcion','tipo']
    
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad', 'created_at', 'updated_at']
    list_filter = ['usuario', 'producto']
    search_fields = ['usuario__username', 'producto__nombre']
    list_per_page = 10


class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'mensaje', 'created_at', 'updated_at']
    search_fields = ['nombre', 'email']
    list_per_page = 10


class HistorialAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad', 'total', 'fecha', 'created_at', 'updated_at']
    list_filter = ['usuario', 'producto']
    search_fields = ['usuario__username', 'producto__nombre']
    list_per_page = 10

class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ['user', 'es_suscriptor', 'descuento', 'created_at', 'updated_at']
    list_filter = ['es_suscriptor']
    search_fields = ['user__username']
    list_per_page = 10

class CuponAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descuento', 'fecha_fin', 'created_at', 'updated_at']
    search_fields = ['codigo']
    list_per_page = 10

admin.site.register(Cupon, CuponAdmin)
admin.site.register(Suscriptor, SuscriptorAdmin)
admin.site.register(Historial, HistorialAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(TipoProducto)
