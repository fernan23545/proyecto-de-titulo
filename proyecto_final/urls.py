from django.contrib import admin
from django.urls import path, include
from marketplace import views as marketplace_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # HOME
    path("", marketplace_views.home_view, name="home"),

    # DIRECTORIO
    path("directorio/<int:pk>/", marketplace_views.emprendimiento_detalle, name="emprendimiento_detalle"),
    path("directorio/", marketplace_views.directory_view, name="directory"),

    # EMPRENDIMIENTOS
    path("emprendimientos/registrar/", marketplace_views.registrar_emprendimiento, name="emprendimiento_registrar"),
    path("mis-emprendimientos/", marketplace_views.mis_emprendimientos, name="mis_emprendimientos"),
    path("emprendimientos/<int:pk>/productos/nuevo/", marketplace_views.crear_producto, name="producto_crear"),

    # MUNICIPAL
    path("municipal/", marketplace_views.panel_municipal, name="panel_municipal"),
    path("municipal/aprobar/<int:pk>/", marketplace_views.aprobar_emprendimiento, name="aprobar_emprendimiento"),
    path("municipal/rechazar/<int:pk>/", marketplace_views.rechazar_emprendimiento, name="rechazar_emprendimiento"),

    # CARRITO
    path("carrito/", marketplace_views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:producto_id>/", marketplace_views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/quitar/<int:producto_id>/", marketplace_views.quitar_del_carrito, name="quitar_del_carrito"),
    path("carrito/vaciar/", marketplace_views.vaciar_carrito, name="vaciar_carrito"),
    path("carrito/agendar-servicio/<int:producto_id>/", marketplace_views.agendar_servicio, name="agendar_servicio"),

    # RESERVAS
    path("mis-reservas/", marketplace_views.mis_reservas, name="mis_reservas"),
    path("reservas/<int:reserva_id>/estado/<str:nuevo_estado>/", marketplace_views.cambiar_estado_reserva, name="cambiar_estado_reserva"),

    # PANEL ADMIN
    path("panel-admin/", marketplace_views.panel_admin, name="panel_admin"),

    # ACCOUNTS
    path("cuenta/", include("accounts.urls")),
    # EDITAR EMPRENDIMIENTO
    path("emprendimiento/<int:pk>/editar/", marketplace_views.emprendimiento_editar, name="emprendimiento_editar"),

# ELIMINAR EMPRENDIMIENTO
    path("emprendimiento/<int:pk>/eliminar/", marketplace_views.emprendimiento_eliminar, name="emprendimiento_eliminar"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
