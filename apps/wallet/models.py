from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    
    # Balances
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Currency
    currency = models.CharField(max_length=3, default='KES')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f"{self.user.email} - Wallet"
    
    def add_pending(self, amount):
        """Add amount to pending balance"""
        self.pending_balance += amount
        self.total_earnings += amount
        self.save()
    
    def approve_earnings(self, amount):
        """Move amount from pending to available"""
        if self.pending_balance >= amount:
            self.pending_balance -= amount
            self.available_balance += amount
            self.save()
            return True
        return False
    
    def withdraw(self, amount):
        """Withdraw amount from available balance"""
        if self.available_balance >= amount:
            self.available_balance -= amount
            self.total_withdrawn += amount
            self.save()
            return True
        return False


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('earning', 'Earning'),
        ('withdrawal', 'Withdrawal'),
        ('refund', 'Refund'),
        ('bonus', 'Bonus'),
        ('penalty', 'Penalty'),
        ('course_purchase', 'Course Purchase'),
        ('course_earning', 'Course Earning'),
        ('survey_reward', 'Survey Reward'),
        ('task_payment', 'Task Payment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Description
    description = models.TextField()
    reference_id = models.CharField(max_length=255, blank=True, null=True)  # External reference
    
    # Related objects
    survey_response = models.ForeignKey('surveys.SurveyResponse', on_delete=models.SET_NULL, null=True, blank=True)
    task_submission = models.ForeignKey('tasks.TaskSubmission', on_delete=models.SET_NULL, null=True, blank=True)
    course_enrollment = models.ForeignKey('courses.Enrollment', on_delete=models.SET_NULL, null=True, blank=True)
    withdrawal_request = models.ForeignKey('WithdrawalRequest', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Fee
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"
    
    def complete(self):
        """Mark transaction as completed"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
        
        # Update wallet
        wallet, created = Wallet.objects.get_or_create(user=self.user)
        
        if self.transaction_type in ['earning', 'bonus', 'course_earning', 'survey_reward', 'task_payment']:
            wallet.approve_earnings(self.net_amount)
        elif self.transaction_type == 'withdrawal':
            wallet.withdraw(self.net_amount)


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    WITHDRAWAL_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('airtel', 'Airtel Money'),
        ('bank', 'Bank Transfer'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='withdrawal_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Method
    withdrawal_method = models.CharField(max_length=20, choices=WITHDRAWAL_METHODS)
    
    # Payment Details
    phone_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Fee
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Processing
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_withdrawals'
    )
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # M-Pesa transaction ID
    receipt_number = models.CharField(max_length=255, blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} via {self.withdrawal_method}"
    
    def calculate_fee(self):
        """Calculate withdrawal fee based on settings"""
        from django.conf import settings
        min_withdrawal = settings.MINIMUM_WITHDRAWAL
        fee_percentage = settings.WITHDRAWAL_FEE_PERCENTAGE
        
        if self.amount < min_withdrawal:
            raise ValueError(f"Minimum withdrawal amount is {min_withdrawal}")
        
        self.fee_amount = self.amount * fee_percentage
        self.net_amount = self.amount - self.fee_amount


class Earning(models.Model):
    SOURCES = [
        ('survey', 'Survey'),
        ('task', 'Task'),
        ('course', 'Course'),
        ('referral', 'Referral'),
        ('bonus', 'Bonus'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earnings')
    source = models.CharField(max_length=20, choices=SOURCES)
    
    # Amount
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Related objects
    survey_response = models.ForeignKey('surveys.SurveyResponse', on_delete=models.SET_NULL, null=True, blank=True)
    task_submission = models.ForeignKey('tasks.TaskSubmission', on_delete=models.SET_NULL, null=True, blank=True)
    course_enrollment = models.ForeignKey('courses.Enrollment', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.source} - {self.amount}"


class BalanceHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='balance_history')
    
    # Balances at this point in time
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Change
    change_amount = models.DecimalField(max_digits=12, decimal_places=2)
    change_type = models.CharField(max_length=20)  # 'credit' or 'debit'
    reason = models.CharField(max_length=255)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.change_type} {self.change_amount}"
