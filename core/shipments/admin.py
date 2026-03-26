from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    # Admin screen par kya-kya dikhega
    list_display = ('bilty_number', 'material_name', 'vehicle', 'total_freight', 'is_paid', 'created_at')
    
    # Side mein filter lagane ke liye
    list_filter = ('is_paid', 'origin', 'destination')
    
    # Search karne ke liye
    search_fields = ('bilty_number', 'material_name')
    
    # Bilty number aur Total Freight ko edit nahi kar sakte (Read-only)
    readonly_fields = ('bilty_number', 'total_freight')