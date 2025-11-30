# marketplace/models.py
from django.db import models
from django.conf import settings


# ============================================================
#  EMRENDIMIENTO
# ============================================================
class Emprendimiento(models.Model):

    CATEGORIAS = [
        ("comida", "Comida / Delivery"),
        ("ropa", "Ropa / Boutique"),
        ("tienda", "Tienda general"),
        ("alimentos", "Alimentos"),
        ("servicios", "Servicios (peluquería, uñas, etc.)"),
        ("otros", "Otros"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emprendimientos"
    )

    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    rubro = models.CharField(max_length=150, blank=True)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email_contacto = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)

    # Imagen principal
    imagen = models.ImageField(upload_to="emprendimientos/", blank=True, null=True)

    # Slider destacado
    imagen1 = models.ImageField(upload_to="emprendimientos/", blank=True, null=True)
    imagen2 = models.ImageField(upload_to="emprendimientos/", blank=True, null=True)
    imagen3 = models.ImageField(upload_to="emprendimientos/", blank=True, null=True)

    permite_agendar = models.BooleanField(default=False)
    permite_compras = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)
    visitas = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.categoria == "comida":
            self.permite_agendar = False
            self.permite_compras = True

        elif self.categoria in ["ropa", "tienda", "alimentos"]:
            self.permite_agendar = False
            self.permite_compras = True

        elif self.categoria == "servicios":
            self.permite_agendar = True
            self.permite_compras = False

        else:
            self.permite_agendar = False
            self.permite_compras = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


# ============================================================
#  PRODUCTOS
# ============================================================
class Producto(models.Model):

    TIPO_CHOICES = [
        ("menu", "Plato / Menú"),
        ("producto", "Producto"),
        ("servicio", "Servicio"),
    ]

    emprendimiento = models.ForeignKey(
        "Emprendimiento",
        on_delete=models.CASCADE,
        related_name="productos"
    )

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="producto")

    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)

    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ============================================================
#  RESERVAS
# ============================================================
class Reserva(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("completado", "Completado"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas"
    )

    emprendimiento = models.ForeignKey(
        Emprendimiento,
        on_delete=models.CASCADE,
        related_name="reservas"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservas"
    )

    nombre_cliente = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    servicio = models.CharField(max_length=200, blank=True)

    fecha = models.DateField()
    hora = models.TimeField()
    comentario = models.TextField(blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva {self.nombre_cliente} - {self.emprendimiento.nombre}"


# ============================================================
#  CARRITO
# ============================================================
class CarritoItem(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carrito_items"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="carrito_items"
    )

    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} ({self.user.username})"
