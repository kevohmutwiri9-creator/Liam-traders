from rest_framework import serializers
from .models import Wallet, Transaction, WithdrawalRequest, Earning, BalanceHistory


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['user', 'total_earnings', 'total_withdrawn', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'status', 'fee_amount', 'net_amount', 'created_at', 'updated_at', 'completed_at']


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'
        read_only_fields = ['user', 'status', 'fee_amount', 'net_amount', 'processed_by',
                          'transaction_id', 'receipt_number', 'created_at', 'updated_at', 'processed_at']


class WithdrawalRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'withdrawal_method', 'phone_number', 'account_name', 'bank_name', 'account_number', 'notes']
    
    def validate(self, attrs):
        user = self.context['request'].user
        amount = attrs['amount']
        
        # Check if user has sufficient balance
        wallet, created = Wallet.objects.get_or_create(user=user)
        if wallet.available_balance < amount:
            raise serializers.ValidationError("Insufficient available balance")
        
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        withdrawal = WithdrawalRequest(user=user, **validated_data)
        
        # Calculate fee
        withdrawal.calculate_fee()
        
        # Deduct from wallet
        wallet, created = Wallet.objects.get_or_create(user=user)
        if wallet.withdraw(withdrawal.amount):
            withdrawal.save()
            
            # Create transaction
            Transaction.objects.create(
                user=user,
                transaction_type='withdrawal',
                amount=withdrawal.amount,
                description=f"Withdrawal via {withdrawal.withdrawal_method}",
                fee_amount=withdrawal.fee_amount,
                net_amount=withdrawal.net_amount,
                withdrawal_request=withdrawal
            )
            
            return withdrawal
        
        raise serializers.ValidationError("Failed to process withdrawal")


class EarningSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Earning
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'is_paid', 'created_at', 'approved_at', 'paid_at']


class BalanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceHistory
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class WithdrawalRequestProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['status', 'transaction_id', 'receipt_number', 'rejection_reason']
