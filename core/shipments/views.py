from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum, Q 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from xhtml2pdf import pisa
from .models import Shipment
from .forms import ShipmentForm

# ==========================================
# 1. AUTHENTICATION VIEWS
# ==========================================

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'shipments/signup.html', {'form': form})


# ==========================================
# 2. MAIN DASHBOARD (With Advanced Analytics)
# ==========================================

def dashboard(request):
    # --- SEARCH & FILTER LOGIC ---
    query = request.GET.get('q', '')
    
    # Backend Power: Complex Q filters for searching across multiple fields
    shipments = Shipment.objects.all().order_by('-created_at')
    
    if query:
        shipments = shipments.filter(
            Q(bilty_number__icontains=query) | 
            Q(material_name__icontains=query) |
            Q(consignor_name__icontains=query) |
            Q(consignee_name__icontains=query) |
            Q(origin__icontains=query) |
            Q(destination__icontains=query)
        )

    # --- FORM HANDLING ---
    form = ShipmentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
        
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save() # Hamara model ka save() method calculations handle kar lega
            return redirect('dashboard')

    # --- INITIAL CONTEXT ---
    context = {
        'shipments': shipments,
        'form': form,
        'query': query,
    }

    # --- BACKEND ANALYTICS (Aggregation) ---
    # Sirf login user ko total financial data dikhega
    if request.user.is_authenticated:
        # Ek hi query mein saare stats nikalna (Performance efficient)
        analytics = shipments.aggregate(
            total_rev=Sum('total_freight'),
            total_exp=Sum('purchase_cost'),
            total_prof=Sum('net_profit')
        )
        
        # Pending dues calculation
        pending = shipments.filter(is_paid=False).aggregate(total_pend=Sum('total_freight'))

        context.update({
            'total_revenue': analytics['total_rev'] or 0,
            'total_expense': analytics['total_exp'] or 0,
            'total_net_profit': analytics['total_prof'] or 0,
            'pending_amount': pending['total_pend'] or 0,
        })

    return render(request, 'shipments/dashboard.html', context)


# ==========================================
# 3. SHIPMENT OPERATIONS (Edit, Delete, PDF)
# ==========================================

@login_required
def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    if request.method == 'POST':
        # instance=shipment zaroori hai update karne ke liye
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save() # Automatic calculations yahan bhi trigger hongi
            return redirect('dashboard')
    else:
        form = ShipmentForm(instance=shipment)
    
    return render(request, 'shipments/edit_shipment.html', {'form': form, 'shipment': shipment})


def download_bilty(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)
        template_path = 'shipments/bilty_pdf.html' 
        context = {'s': shipment}
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Bilty_{shipment.bilty_number}.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response
    except Shipment.DoesNotExist:
        return HttpResponse('Shipment not found', status=404)


@login_required
def mark_as_paid(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.is_paid = True
    shipment.save()
    return redirect('dashboard')


@login_required
def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.delete()
    return redirect('dashboard')