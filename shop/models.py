from django.db import models

class Car(models.Model):
    FUEL_CHOICES = [
        ('benzin', 'Benzin'),
        ('dizel', 'Dizel'),
        ('elektr', 'Elektr'),
        ('gibrid', 'Gibrid'),
    ]
    TRANSMISSION_CHOICES = [
        ('mexanika', 'Mexanika'),
        ('avtomat', 'Avtomat'),
        ('variator', 'Variator'),
    ]
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='benzin')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    engine_volume = models.FloatField(verbose_name="Dvigatel hajmi")
    color = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    class Meta:
        verbose_name = "Avtomobil"
        verbose_name_plural = "Avtomobillar"