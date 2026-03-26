from django.urls import path
from django.contrib.auth import views as auth_views # Login/Logout ke liye
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # Isse home page dashboard ban jayega
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='shipments/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('download/<int:shipment_id>/', views.download_bilty, name='download_bilty'),
    path('paid/<int:shipment_id>/', views.mark_as_paid, name='mark_as_paid'),
    path('delete/<int:shipment_id>/', views.delete_shipment, name='delete_shipment'),
]