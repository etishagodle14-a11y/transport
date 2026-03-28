from django.db import models
from django.core.exceptions import ValidationError
from fleet.models import Vehicle, Driver 

class Shipment(models.Model):
    # --- BASIC DETAILS ---
    bilty_number = models.CharField(max_length=20, unique=True, editable=False)
    material_name = models.CharField(max_length=100)
    
    # --- COMPANY DETAILS ---
    consignor_name = models.CharField(max_length=200, default="Unknown", verbose_name="Sender Company") 
    consignee_name = models.CharField(max_length=200, default="Unknown", verbose_name="Receiver Company")

    # --- RELATIONSHIPS ---
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    
    # --- ROUTE & WEIGHT ---
    origin = models.CharField(max_length=100) 
    destination = models.CharField(max_length=100) 
    distance_km = models.PositiveIntegerField(default=0, null=True, blank=True)
    
    # --- LOGISTICS OPTIONS ---
    BOOKING_CHOICES = [
        ('pickup', 'Company Pickup'),
        ('drop', 'Customer Drop at Transport'),
    ]
    DELIVERY_CHOICES = [
        ('door', 'Door Delivery'),
        ('office', 'Office Collection'),
    ]
    
    booking_type = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='drop')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='office')

    # --- ACCOUNTS & CALCULATIONS ---
    weight_tonnes = models.FloatField(default=0)
    rate_per_tonne = models.FloatField(default=0)
    total_freight = models.FloatField(default=0, editable=False) # Total Sale (Automatic)

    # Expense Fields (Purchase breakdown)
    diesel_expenses = models.FloatField(default=0)
    toll_expenses = models.FloatField(default=0)
    driver_allowance = models.FloatField(default=0)
    other_expenses = models.FloatField(default=0)
    
    # Automatic Sum Fields
    purchase_cost = models.FloatField(default=0, editable=False) # Total Expense (Automatic)
    net_profit = models.FloatField(default=0, editable=False)   # Final Profit (Automatic)

    # --- STATUS & TIME ---
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- BACKEND LOGIC (SAVE METHOD OVERRIDE) ---
    def save(self, *args, **kwargs):
        # 1. Validation: Backend level par galti rokna
        if self.weight_tonnes < 0 or self.rate_per_tonne < 0:
            raise ValidationError("Weight or Rate cannot be negative!")
        
        if self.diesel_expenses < 0 or self.toll_expenses < 0:
            raise ValidationError("Expenses cannot be negative!")

        # 2. Calculation: Python math for Freight
        self.total_freight = float(self.weight_tonnes or 0) * float(self.rate_per_tonne or 0)
        
        # 3. Calculation: Purchase Cost (Total Expenses)
        self.purchase_cost = (
            float(self.diesel_expenses or 0) + 
            float(self.toll_expenses or 0) + 
            float(self.driver_allowance or 0) + 
            float(self.other_expenses or 0)
        )
        
        # 4. Calculation: Net Profit
        self.net_profit = self.total_freight - self.purchase_cost
        
        # 5. ID-Based Bilty Number Generation
        # Naya record hai to hi Bilty generate karein
        if not self.bilty_number:
            last_shipment = Shipment.objects.all().order_by('id').last()
            if not last_shipment:
                self.bilty_number = 'TF-101'
            else:
                new_id = last_shipment.id + 1
                self.bilty_number = f'TF-{new_id:03d}'
        
        # 6. Final Save to Database
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bilty_number} - {self.consignor_name} to {self.consignee_name}"