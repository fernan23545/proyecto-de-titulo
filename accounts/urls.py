# C:\proyecto_final\accounts\urls.py
from django.urls import path
from django.http import HttpResponse
from .views import SignUpView, SignInView, signout_view, dashboard
from . import views

def ok(_):
    return HttpResponse("Accounts OK")   # placeholder temporal

urlpatterns = [
    path("", ok, name="accounts_index"),
    path("ingresar/", SignInView.as_view(), name="login"),
    path("registrar/", SignUpView.as_view(), name="signup"),
    path("salir/", signout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("ingresar/", views.login_view, name="login"),
    #path("registrar/", views.signup_view, name="signup"),

    # PERFIL DEL USUARIO
    path("perfil/", views.profile_view, name="profile"),

    # CERRAR SESIÓN
    path("salir/", views.logout_view, name="logout"),
]
