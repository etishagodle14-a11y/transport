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
    query = request.GET.get('q', '')
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

    form = ShipmentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
        
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('dashboard')

    context = {
        'shipments': shipments,
        'form': form,
        'query': query,
    }

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
# 3. SHIPMENT OPERATIONS (Edit, Delete, PDF)
# ==========================================

@login_required
def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save() 
            return redirect('dashboard')
    else:
        form = ShipmentForm(instance=shipment)
    
    return render(request, 'shipments/edit_shipment.html', {'form': form, 'shipment': shipment})


# --- PDF GENERATION (Sahi context 's' ke saath) ---
def download_bilty(request, shipment_id):
    try:
        shipment = get_object_or_404(Shipment, id=shipment_id)
        template_path = 'shipments/bilty_pdf.html' 
        
        # 's' variable hi pass kiya hai taaki aapka template crash na ho
        context = {'s': shipment}
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Bilty_{shipment.bilty_number}.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=404)


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