from .models import Carrito
from django.db.models import Count

def carrito(request):
    carrito = []
    total_general = 0
    total_productos = 0
    
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user)
        
        for item in carrito:
            item.total = item.producto.precio * item.cantidad
            total_general += item.total
        
        total_productos = carrito.values('producto').annotate(count=Count('producto')).count()

    return {'carrito': carrito, 'total_general': total_general, 'total_productos': total_productos }
