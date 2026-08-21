from django.urls import path
from .views import (
    MpesaPaymentListView, MpesaPaymentDetailView,
    PaymentMethodListCreateView, PaymentMethodDetailView,
    initiate_withdrawal, mpesa_callback, payment_methods, transaction_logs
)

urlpatterns = [
    path('mpesa/', MpesaPaymentListView.as_view(), name='mpesa-payments'),
    path('mpesa/<int:pk>/', MpesaPaymentDetailView.as_view(), name='mpesa-payment-detail'),
    path('mpesa/withdraw/', initiate_withdrawal, name='initiate-withdrawal'),
    path('mpesa/callback/', mpesa_callback, name='mpesa-callback'),
    path('methods/', payment_methods, name='payment-methods'),
    path('methods/', PaymentMethodListCreateView.as_view(), name='payment-methods-list'),
    path('methods/<int:pk>/', PaymentMethodDetailView.as_view(), name='payment-method-detail'),
    path('admin/logs/', transaction_logs, name='transaction-logs'),
]
