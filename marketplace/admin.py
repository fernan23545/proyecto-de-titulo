from django.contrib import admin
from .models import Emprendimiento, Producto, Reserva, CarritoItem

# -----------------------------
# EMPRENDIMIENTOS
# -----------------------------
@admin.register(Emprendimiento)
class EmprendimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "owner", "is_verified")
    list_filter = ("categoria", "is_verified")
    search_fields = ("nombre", "rubro", "direccion")
    actions = ["delete_selected"]
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        # renombrar acción por claridad
        if "delete_selected" in actions:
            actions["delete_selected"][0].short_description = "Eliminar emprendimientos seleccionados"
        return actions

# -----------------------------
# PRODUCTOS
# -----------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "emprendimiento", "tipo", "precio", "disponible")
    list_filter = ("tipo", "disponible")
    search_fields = ("nombre",)

# -----------------------------
# RESERVAS
# -----------------------------
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("emprendimiento", "nombre_cliente", "fecha", "hora", "servicio")
    list_filter = ("emprendimiento", "fecha")
    search_fields = ("nombre_cliente", "servicio")

# -----------------------------
# CARRITO ITEMS
# -----------------------------
@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ("producto", "user", "cantidad")
    list_filter = ("user",)
    search_fields = ("producto__nombre", "user__username")
    

    

