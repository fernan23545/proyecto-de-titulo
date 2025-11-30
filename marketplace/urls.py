from django.urls import path
from .views import registrar_emprendimiento, directory_view
from accounts import views as accounts_views
from . import views


urlpatterns = [
    # Registrar
    path("registrar/", registrar_emprendimiento, name="emprendimiento_registrar"),

    # Directorio
    path("directorio/", directory_view, name="directory"),

    # 🔥 DETALLE (FALTABA ESTA RUTA)
    path("directorio/<int:pk>/", views.emprendimiento_detalle, name="emprendimiento_detalle"),

    # Cuenta
    path("cuenta/ingresar/", accounts_views.login_view, name="login"),
    path("cuenta/registro/", accounts_views.SignUpView.as_view(), name="signup"),
    path("cuenta/perfil/", accounts_views.profile_view, name="profile"),
    path("cuenta/salir/", accounts_views.logout_view, name="logout"),

    # Editar / Eliminar
    path("emprendimiento/<int:pk>/editar/", views.emprendimiento_editar, name="emprendimiento_editar"),
    path("emprendimiento/<int:pk>/eliminar/", views.emprendimiento_eliminar, name="emprendimiento_eliminar"),
    # EDITAR PRODUCTO
    path("producto/<int:producto_id>/editar/", views.producto_editar, name="producto_editar"),

    # ELIMINAR PRODUCTO
    path("producto/<int:producto_id>/eliminar/", views.producto_eliminar, name="producto_eliminar"),

]
