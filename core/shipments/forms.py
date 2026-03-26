from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        # 1. Sabhi fields ko list mein add kiya gaya hai
        fields = [
            'consignor_name', 'consignee_name', 'material_name', 
            'vehicle', 'driver', 'origin', 'destination', 
            'distance_km', 'weight_tonnes', 'rate_per_tonne', 
            'booking_type', 'delivery_type', 
            'diesel_expenses', 'toll_expenses', 'driver_allowance', 'other_expenses',
            'is_paid'
        ]
        
        # 2. Har field ke liye Bootstrap classes aur placeholders
        widgets = {
            # Company Details
            'consignor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sender Company Name'}),
            'consignee_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Company Name'}),
            
            # Basic Details
            'material_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Material Name'}),
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            
            # Route
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From City'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To City'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total KM'}),
            
            # Pricing & Logistics
            'weight_tonnes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (MT)'}),
            'rate_per_tonne': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate per Tonne'}),
            'booking_type': forms.Select(attrs={'class': 'form-select'}),
            'delivery_type': forms.Select(attrs={'class': 'form-select'}),
            
            # Expenses (Purchase)
            'diesel_expenses': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Diesel ₹'}),
            'toll_expenses': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Toll ₹'}),
            'driver_allowance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary/Food ₹'}),
            'other_expenses': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Others ₹'}),
            
            # Status
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }