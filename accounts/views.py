from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm
from .models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse

# -----------------------------
# LOGIN USANDO LoginView (no lo estás usando)
# -----------------------------
class SignInView(LoginView):
    template_name = "accounts/login.html"

# -----------------------------
# REGISTRO
# -----------------------------
class SignUpView(View):
    def get(self, request):
        return render(request, "accounts/signup.html", {"form": SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # ⚠️ YA NO REDIRIGE AL DASHBOARD
            return redirect("profile")
        return render(request, "accounts/signup.html", {"form": form})


# -----------------------------
# LOGOUT
# -----------------------------
def signout_view(request):
    logout(request)
    return redirect("home")


# -----------------------------
# DASHBOARD (NO SE ELIMINA)
# MANTIENE FUNCIONES, PERO YA NO SE USA COMO REDIRECCIÓN
# -----------------------------
@login_required
def dashboard(request):
    """
    Mantiene la lógica de roles,
    pero no se llama automáticamente después de login o signup.
    """
    return redirect("profile")
# -----------------------------
# LOGIN PERSONALIZADO
# -----------------------------
def login_view(request):
    next_url = request.GET.get("next", "")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Si venía desde carrito u otra página
            if next_url:
                return redirect(next_url)

            # ⚠️ YA NO REDIRIGE AL DASHBOARD
            return redirect("profile")

        return render(request, "accounts/login.html", {
            "error": "Usuario o contraseña incorrectos",
            "next": next_url,
        })

    return render(request, "accounts/login.html", {"next": next_url})


# -----------------------------
# PERFIL DEL USUARIO
# -----------------------------
from marketplace.models import Reserva

@login_required
def profile_view(request):
    usuario = request.user
    
    # Reservas hechas por este usuario
    reservas_cliente = Reserva.objects.filter(
        usuario=usuario
    ).order_by("-fecha", "-hora")

    return render(request, "accounts/profile.html", {
        "reservas_cliente": reservas_cliente
    })

# -----------------------------
# CERRAR SESIÓN
# -----------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect("home")
