# marketplace/forms.py
from django import forms
from .models import Emprendimiento, Producto, Reserva


class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = [
            "nombre",
            "categoria",
            "rubro",
            "descripcion",
            "direccion",
            "telefono",
            "email_contacto",
            "sitio_web",
            "imagen",
            "imagen1",
            "imagen2",
            "imagen3",
        ]
        widgets = {
            field: forms.TextInput(attrs={"class": "form-input"})
            for field in ["nombre", "rubro", "direccion", "telefono"]
        }
        widgets.update({
            "descripcion": forms.Textarea(attrs={"class": "form-input"}),
            "email_contacto": forms.EmailInput(attrs={"class": "form-input"}),
            "sitio_web": forms.URLInput(attrs={"class": "form-input"}),
            "categoria": forms.Select(attrs={"class": "form-input"}),
        })


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["tipo", "nombre", "descripcion", "precio", "imagen"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-input"}),
            "nombre": forms.TextInput(attrs={"class": "form-input"}),
            "descripcion": forms.Textarea(attrs={"class": "form-input"}),
            "precio": forms.NumberInput(attrs={"class": "form-input"}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-input"}),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            "nombre_cliente",
            "telefono",
            "email",
            "servicio",
            "fecha",
            "hora",
            "comentario",
        ]
