from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ("M", "Erkak"),
        ("F", "Ayol"),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"