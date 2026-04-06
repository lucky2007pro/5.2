from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    car = models.ForeignKey(
        'shop.Car',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='users'
    )

    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"