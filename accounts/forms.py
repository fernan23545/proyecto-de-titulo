from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150, required=True)
    last_name  = forms.CharField(label="Apellido", max_length=150, required=False)
    email      = forms.EmailField(label="Correo", required=True)
    phone      = forms.CharField(label="Teléfono", max_length=20, required=False)
    username   = forms.CharField(label="Usuario", max_length=150, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "username", "password1", "password2")
        help_texts = {f: "" for f in fields}
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases Tailwind a todos los widgets
        for field in self.fields.values():
            classes = "mt-1 block w-full border rounded px-3 py-2"
            # conserva clases existentes si las hay
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " " + classes).strip()
