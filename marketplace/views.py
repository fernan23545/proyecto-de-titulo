from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Count, Sum
from .models import Emprendimiento, Producto, Reserva, CarritoItem
from .forms import EmprendimientoForm, ProductoForm, ReservaForm
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta



@login_required
def emprendimiento_eliminar(request, pk):
    emprendimiento = get_object_or_404(Emprendimiento, pk=pk)

    # Solo administradores pueden eliminar
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para eliminar este emprendimiento.")
        return redirect("emprendimiento_detalle", pk=pk)

    if request.method == "POST":
        emprendimiento.delete()
        messages.success(request, "Emprendimiento eliminado correctamente.")
        return redirect("directory")

    return render(request, "marketplace/emprendimiento_confirmar_eliminar.html", {
        "emprendimiento": emprendimiento
    })

# ==========================
# HOME
# ==========================

def home_view(request):

    emprendimientos = Emprendimiento.objects.filter(is_verified=True)

    # Agrupar por categoría EN PYTHON (lo correcto)
    categorias_dict = {}
    for e in emprendimientos:
        if e.categoria not in categorias_dict:
            categorias_dict[e.categoria] = []
        categorias_dict[e.categoria].append(e)

    # Imágenes del slider
    hero_images = [
        "https://www.diariopaillaco.cl/files/673282a948988_1200x719.jpg",
        "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
        "https://www.diarioemprende.cl/files/68928d616617a_1200x719.jpg",
        "https://www.diariopaillaco.cl/files/6545669297be7_890x533.jpg",
        
    ]

    return render(request, "home.html", {
        "emprendimientos_home": emprendimientos,
        "categorias": Emprendimiento.CATEGORIAS,
        "categorias_dict": categorias_dict,   # ← ESTA LÍNEA ES LA IMPORTANTE
        "hero_images": hero_images,
    })


# ==========================
# DIRECTORIO
# ==========================
def directory_view(request):
    categorias = dict(Emprendimiento.CATEGORIAS)

    emprendimientos = Emprendimiento.objects.filter(is_verified=True)

    # Agrupar por categoría
    agrupados = {}
    for key, label in categorias.items():
        lista = emprendimientos.filter(categoria=key)
        if lista.exists():
            agrupados[label] = lista

    return render(
        request,
        "directory.html",
        {
            "agrupados": agrupados,
            "categorias": categorias,
            "emprendimientos": emprendimientos,
        },
    )


# ==========================
# DETALLE DE EMPRENDIMIENTO
# ==========================
def emprendimiento_detalle(request, pk):
    emprendimiento = get_object_or_404(Emprendimiento, pk=pk)

    # Contador de visitas
    emprendimiento.visitas = (emprendimiento.visitas or 0) + 1
    emprendimiento.save(update_fields=["visitas"])

    # Todos los productos
    productos_qs = Producto.objects.filter(emprendimiento=emprendimiento)

    # --- 1) Menú tipo comida ---
    menu_items = None
    if emprendimiento.categoria == "comida":
        menu_items = productos_qs.filter(tipo="menu")

    # --- 2) Productos generales (ropa, tienda, alimentos) ---
    productos_generales = None
    if emprendimiento.categoria in ["ropa", "tienda", "alimentos"]:
        productos_generales = productos_qs.filter(tipo="producto")

    # --- 3) Servicios (categoría = "servicios") ---
    servicios_ofrecidos = None
    reserva_form = None
    mensaje_reserva = None

    if emprendimiento.categoria == "servicios":   # ← CORREGIDO
        servicios_ofrecidos = productos_qs.filter(tipo="servicio")

        if request.method == "POST":
            reserva_form = ReservaForm(request.POST)
            if reserva_form.is_valid():
                reserva = reserva_form.save(commit=False)
                reserva.emprendimiento = emprendimiento
                reserva.save()
                mensaje_reserva = "Solicitud de reserva enviada correctamente."
                reserva_form = ReservaForm()
        else:
            reserva_form = ReservaForm()

    context = {
        "emprendimiento": emprendimiento,
        "menu_items": menu_items,
        "productos_generales": productos_generales,
        "servicios_ofrecidos": servicios_ofrecidos,
        "reserva_form": reserva_form,
        "mensaje_reserva": mensaje_reserva,
    }

    return render(request, "marketplace/emprendimiento_detalle.html", context)

# ==========================
# REGISTRAR EMPRENDIMIENTO
# ==========================
@login_required(login_url="/cuenta/ingresar/")
def registrar_emprendimiento(request):
    if request.method == "POST":
        form = EmprendimientoForm(request.POST, request.FILES)
        if form.is_valid():
            emprendimiento = form.save(commit=False)
            emprendimiento.owner = request.user
            emprendimiento.save()
            return redirect("mis_emprendimientos")
    else:
        form = EmprendimientoForm()

    return render(request, "marketplace/registrar_emprendimiento.html", {"form": form})


# ==========================
# PANEL MUNICIPAL
# ==========================
def es_municipal(user):
    return user.is_staff and not user.is_superuser

@user_passes_test(es_municipal)
def panel_municipal(request):
    pendientes = Emprendimiento.objects.filter(is_verified=False)
    aprobados = Emprendimiento.objects.filter(is_verified=True)
    return render(request, "municipal/panel.html", {"pendientes": pendientes, "aprobados": aprobados})


@user_passes_test(es_municipal)
def aprobar_emprendimiento(request, pk):
    emp = get_object_or_404(Emprendimiento, pk=pk)
    emp.is_verified = True
    emp.save()
    return redirect("panel_municipal")


@user_passes_test(es_municipal)
def rechazar_emprendimiento(request, pk):
    emp = get_object_or_404(Emprendimiento, pk=pk)
    emp.delete()
    return redirect("panel_municipal")


# ==========================
# MIS EMPRENDIMIENTOS
# ==========================
@login_required
def mis_emprendimientos(request):
    emprendimientos = Emprendimiento.objects.filter(owner=request.user)
    return render(request, "marketplace/mis_emprendimientos.html", {"emprendimientos": emprendimientos})


# ==========================
# CREAR PRODUCTO (CORRECTO ÚNICO)
# ==========================
@login_required
def crear_producto(request, pk):

    emprendimiento = get_object_or_404(Emprendimiento, pk=pk, owner=request.user)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)   # << IMPORTANTE
        if form.is_valid():
            producto = form.save(commit=False)
            producto.emprendimiento = emprendimiento
            producto.save()
            messages.success(request, "Producto / servicio agregado correctamente.")
            return redirect("emprendimiento_detalle", pk=emprendimiento.pk)
    else:
        form = ProductoForm()

    return render(request, "marketplace/producto_form.html", {"form": form, "emprendimiento": emprendimiento})


# ==========================
# CARRITO
# ==========================
def _get_cart(request):
    return request.session.get("cart", [])

def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


@require_POST
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = _get_cart(request)

    for item in cart:
        if item["producto_id"] == producto.id:
            item["cantidad"] += 1
            break
    else:
        cart.append({"producto_id": producto.id, "cantidad": 1})

    _save_cart(request, cart)
    return redirect("emprendimiento_detalle", pk=producto.emprendimiento.pk)


@login_required
def ver_carrito(request):
    cart = _get_cart(request)
    ids = [item["producto_id"] for item in cart]
    productos = Producto.objects.filter(id__in=ids)

    items = []
    total = 0

    for prod in productos:
        cantidad = next((i["cantidad"] for i in cart if i["producto_id"] == prod.id), 1)
        subtotal = prod.precio * cantidad
        total += subtotal
        items.append({"producto": prod, "cantidad": cantidad, "subtotal": subtotal})

    return render(request, "marketplace/carrito.html", {"items": items, "total": total})


# ==========================
# AGENDA
# ==========================
@login_required
def agendar_servicio(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, tipo="servicio")
    emprendimiento = producto.emprendimiento

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.emprendimiento = emprendimiento
            reserva.servicio = producto.nombre
            reserva.save()
            return redirect("emprendimiento_detalle", pk=emprendimiento.pk)
    else:
        form = ReservaForm(initial={"servicio": producto.nombre})

    return render(request, "marketplace/agendar_servicio.html", {"form": form, "producto": producto})


# ==========================
# RESERVAS
# ==========================
@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(emprendimiento__owner=request.user).select_related("emprendimiento","producto")
    return render(request, "marketplace/mis_reservas.html", {"reservas": reservas})


@login_required
def cambiar_estado_reserva(request, reserva_id, nuevo_estado):
    reserva = get_object_or_404(Reserva, id=reserva_id, emprendimiento__owner=request.user)

    if nuevo_estado not in {"pendiente","en_proceso","completado","cancelado"}:
        return redirect("mis_reservas")

    reserva.estado = nuevo_estado
    reserva.save()
    return redirect("mis_reservas")


# ==========================
# PANEL ADMIN
# ==========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def panel_admin(request):
   

    User = get_user_model()

    # Métricas principales
    total_usuarios = User.objects.count()
    total_emprendimientos = Emprendimiento.objects.count()
    total_verificados = Emprendimiento.objects.filter(is_verified=True).count()
    total_no_verificados = Emprendimiento.objects.filter(is_verified=False).count()
    total_reservas = Reserva.objects.count()

    total_visitas = (
        Emprendimiento.objects.aggregate(total=Sum("visitas"))["total"] or 0
    )

    # Emprendimientos nuevos por mes (últimos 6 meses)
    hoy = now().date()
    meses = []
    nuevos_por_mes = []

    for i in range(5, -1, -1):
        mes = (hoy.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        siguiente = (mes + timedelta(days=32)).replace(day=1)

        count = Emprendimiento.objects.filter(
            creado_en__gte=mes,
            creado_en__lt=siguiente,
        ).count()

        meses.append(mes.strftime("%b %Y"))
        nuevos_por_mes.append(count)

    # Categorías (pie chart)
    categorias_qs = (
        Emprendimiento.objects.values("categoria")
        .annotate(cantidad=Count("id"))
        .order_by("categoria")
    )

    categorias_labels = [c["categoria"] for c in categorias_qs]
    categorias_cantidad = [c["cantidad"] for c in categorias_qs]

    # Reservas por estado
    reservas_qs = (
        Reserva.objects.values("estado")
        .annotate(cantidad=Count("id"))
        .order_by("estado")
    )

    reservas_labels = [r["estado"] for r in reservas_qs]
    reservas_cantidad = [r["cantidad"] for r in reservas_qs]

    # Top 5 emprendimientos por visitas
    top_emprendimientos = (
        Emprendimiento.objects.filter(visitas__gt=0)
        .order_by("-visitas")[:5]
    )

    return render(
        request,
        "panel_admin.html",
        {
            "total_usuarios": total_usuarios,
            "total_emprendimientos": total_emprendimientos,
            "total_verificados": total_verificados,
            "total_no_verificados": total_no_verificados,
            "total_reservas": total_reservas,
            "total_visitas": total_visitas,

            # gráficos
            "meses": meses,
            "nuevos_por_mes": nuevos_por_mes,
            "categorias_labels": categorias_labels,
            "categorias_cantidad": categorias_cantidad,
            "reservas_labels": reservas_labels,
            "reservas_cantidad": reservas_cantidad,

            # top
            "top_emprendimientos": top_emprendimientos,
        },
    )

# ==========================
# QUITAR 1 PRODUCTO DEL CARRITO
# ==========================
@require_POST
def quitar_del_carrito(request, producto_id):
    cart = _get_cart(request)
    nuevo_carrito = []

    for item in cart:
        if item["producto_id"] == producto_id:
            if item["cantidad"] > 1:
                item["cantidad"] -= 1  # resta 1
                nuevo_carrito.append(item)
            # si era 1, no lo agregamos (lo elimino)
        else:
            nuevo_carrito.append(item)

    _save_cart(request, nuevo_carrito)
    messages.info(request, "Producto actualizado en el carrito.")
    return redirect("ver_carrito")


# ==========================
# VACIAR TODO EL CARRITO
# ==========================
@require_POST
def vaciar_carrito(request):
    _save_cart(request, [])
    messages.info(request, "Carrito vaciado.")
    return redirect("ver_carrito")
@login_required
def emprendimiento_editar(request, pk):
    emprendimiento = get_object_or_404(Emprendimiento, pk=pk, owner=request.user)

    if request.method == "POST":
        form = EmprendimientoForm(request.POST, request.FILES, instance=emprendimiento)
        if form.is_valid():
            form.save()
            return redirect("emprendimiento_detalle", pk=pk)
    else:
        form = EmprendimientoForm(instance=emprendimiento)

    return render(request, "marketplace/emprendimiento_form.html", {
        "form": form,
        "emprendimiento": emprendimiento
    })
@login_required
def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, emprendimiento__owner=request.user)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("emprendimiento_detalle", pk=producto.emprendimiento.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(request, "marketplace/producto_form.html", {
        "form": form,
        "emprendimiento": producto.emprendimiento,
        "edit_mode": True,
    })


@login_required
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, emprendimiento__owner=request.user)

    if request.method == "POST":
        pk = producto.emprendimiento.pk
        producto.delete()
        messages.success(request, "Producto eliminado.")
        return redirect("emprendimiento_detalle", pk=pk)

    return render(request, "marketplace/producto_confirmar_eliminar.html", {
        "producto": producto
    })
