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
# 1. AUTHENTICATION VIEWS (Signup)
# ==========================================

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Account banane ke baad auto-login
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    # Aapka custom path: shipments/signup.html
    return render(request, 'shipments/signup.html', {'form': form})


# ==========================================
# 2. MAIN DASHBOARD (Public + Private Logic)
# ==========================================

def dashboard(request):
    # --- SEARCH LOGIC ---
    query = request.GET.get('q')
    if query:
        shipments = Shipment.objects.filter(
            Q(bilty_number__icontains=query) | 
            Q(material_name__icontains=query) |
            Q(consignor_name__icontains=query) |
            Q(origin__icontains=query) |
            Q(destination__icontains=query)
        ).order_by('-created_at')
    else:
        shipments = Shipment.objects.all().order_by('-created_at')

    # --- NEW BOOKING FORM (Sirf Login User ke liye) ---
    form = ShipmentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') # Bina login entry allowed nahi hai
        
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    # --- INITIAL CONTEXT ---
    context = {
        'shipments': shipments,
        'form': form,
        'query': query,
    }

    # --- ANALYTICS (Sirf Login User ke liye) ---
    if request.user.is_authenticated:
        analytics = shipments.aggregate(
            total_rev=Sum('total_freight'),
            total_exp=Sum('purchase_cost'),
            total_prof=Sum('net_profit')
        )
        pending = shipments.filter(is_paid=False).aggregate(total_pend=Sum('total_freight'))

        context.update({
            'total_revenue': analytics['total_rev'] or 0,
            'total_expense': analytics['total_exp'] or 0,
            'total_net_profit': analytics['total_prof'] or 0,
            'pending_amount': pending['total_pend'] or 0,
        })

    return render(request, 'shipments/dashboard.html', context)


# ==========================================
# 3. SHIPMENT OPERATIONS (Secure Views)
# ==========================================

# PDF Download View
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


# Mark As Paid (Login required for security)
@login_required
def mark_as_paid(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.is_paid = True
    shipment.save()
    return redirect('dashboard')


# Delete Shipment (Login required for security)
@login_required
def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.delete()
    return redirect('dashboard')