from .models import *
from rest_framework import serializers


class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model= TipoProducto
        fields= '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    
    tipo = TipoProductoSerializer(read_only=True)
    #aqui añadir claves foraneas
    class Meta:
        model= Producto
        fields= '__all__'
