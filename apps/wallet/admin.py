from django.contrib import admin
from .models import Wallet, Transaction, WithdrawalRequest, Earning, BalanceHistory


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'pending_balance', 'available_balance', 'total_earnings', 'total_withdrawn', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'status', 'amount', 'fee_amount', 'net_amount', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__email', 'description', 'reference_id']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'withdrawal_method', 'status', 'fee_amount', 'net_amount', 'created_at']
    list_filter = ['status', 'withdrawal_method', 'created_at']
    search_fields = ['user__email', 'phone_number', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at', 'processed_at']


@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ['user', 'source', 'amount', 'is_approved', 'is_paid', 'created_at']
    list_filter = ['source', 'is_approved', 'is_paid', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'approved_at', 'paid_at']


@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'pending_balance', 'available_balance', 'change_amount', 'change_type', 'created_at']
    list_filter = ['change_type', 'created_at']
    search_fields = ['user__email', 'reason']
    readonly_fields = ['created_at']
