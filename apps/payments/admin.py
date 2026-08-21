from django.contrib import admin
from .models import MpesaPayment, PaymentMethod, TransactionLog


@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'status', 'amount', 'phone_number', 'mpesa_receipt_number', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__email', 'phone_number', 'merchant_request_id', 'checkout_request_id']
    readonly_fields = ['merchant_request_id', 'checkout_request_id', 'response_code', 'response_description',
                      'result_code', 'result_description', 'mpesa_receipt_number', 'transaction_date', 'created_at', 'updated_at']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'method_type', 'phone_number', 'account_name', 'is_verified', 'is_default']
    list_filter = ['method_type', 'is_verified', 'is_default']
    search_fields = ['user__email', 'phone_number', 'account_name']


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'method', 'status_code', 'success', 'created_at']
    list_filter = ['method', 'success', 'status_code']
    search_fields = ['endpoint', 'user__email']
    readonly_fields = ['created_at']
