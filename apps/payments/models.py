from django.db import models
from django.conf import settings


class MpesaPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    TRANSACTION_TYPES = [
        ('withdrawal', 'Withdrawal'),
        ('deposit', 'Deposit'),
        ('payment', 'Payment'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mpesa_payments')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Phone Number
    phone_number = models.CharField(max_length=20)
    
    # M-Pesa Details
    merchant_request_id = models.CharField(max_length=255, unique=True)
    checkout_request_id = models.CharField(max_length=255, blank=True, null=True)
    response_code = models.CharField(max_length=10, blank=True, null=True)
    response_description = models.TextField(blank=True, null=True)
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_description = models.TextField(blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=255, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    
    # Related withdrawal request
    withdrawal_request = models.ForeignKey('wallet.WithdrawalRequest', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"


class PaymentMethod(models.Model):
    METHOD_TYPES = [
        ('mpesa', 'M-Pesa'),
        ('airtel', 'Airtel Money'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=20, choices=METHOD_TYPES)
    
    # Payment Details
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
    
    def __str__(self):
        return f"{self.user.email} - {self.method_type}"


class TransactionLog(models.Model):
    """Log all payment-related API calls and responses"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.URLField()
    method = models.CharField(max_length=10)  # GET, POST, etc.
    request_data = models.JSONField(default=dict)
    response_data = models.JSONField(default=dict)
    status_code = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.endpoint} - {self.method}"
