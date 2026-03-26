from django.db import models

class Vehicle(models.Model):
    # Gaadi ke types
    VEHICLE_CHOICES = [
        ('TRUCK', 'Standard Truck'),
        ('TRAILER', 'Trailer'),
        ('CONTAINER', 'Container'),
        ('PICKUP', 'Pickup/Tempo'),
    ]

    vehicle_number = models.CharField(max_length=20, unique=True) # e.g. RJ-14-GB-1234
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, default='TRUCK')
    capacity_tonnes = models.DecimalField(max_digits=5, decimal_places=2) # Kitna load utha sakti hai
    is_available = models.BooleanField(default=True) # Kya gaadi free hai?

    def __str__(self):
        return f"{self.vehicle_number} ({self.vehicle_type})"

class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True) # Kya driver duty par hai?

    def __str__(self):
        return self.name