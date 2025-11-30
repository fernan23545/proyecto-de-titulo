from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        CIUDADANO = "citizen", "Ciudadano"
        EMPRENDEDOR = "entrepreneur", "Emprendedor"
        ADMIN_MUNI = "admin_muni", "Admin. Municipal"

    role = models.CharField(
        max_length=20, choices=Roles.choices, default=Roles.CIUDADANO
        
    )
