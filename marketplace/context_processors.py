# C:\proyecto_final\marketplace\context_processors.py
from .models import CarritoItem
def carrito_count(request):
    """
    Devuelve la cantidad total de ítems en el carrito
    usando la sesión del usuario.
    """
    carrito = request.session.get("carrito", {})

    total = 0
    for item in carrito.values():
        # cada item es un dict: {"producto_id": ..., "cantidad": ...}
        cantidad = item.get("cantidad", 1)
        total += cantidad

    return {"carrito_count": total}


# marketplace/context_processors.py
from .models import CarritoItem


def carrito_context(request):
    """
    Devuelve la cantidad de ítems en el carrito para mostrarla en la barra superior.
    """
    count = 0

    if request.user.is_authenticated:
        # 👇 el campo correcto es 'user', NO 'usuario'
        count = CarritoItem.objects.filter(user=request.user).count()
    else:
        # Si no está autenticado, contamos los ítems guardados en la sesión
        cart = request.session.get("cart", [])
        count = sum(item.get("cantidad", 1) for item in cart)

    return {"carrito_count": count}
