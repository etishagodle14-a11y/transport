from django.contrib import admin
from .models import Vehicle, Driver

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'vehicle_type', 'capacity_tonnes', 'is_available')
    list_filter = ('vehicle_type', 'is_available')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'phone_number', 'is_active')