from rest_framework import serializers
from .models import MpesaPayment, PaymentMethod, TransactionLog


class MpesaPaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = MpesaPayment
        fields = '__all__'
        read_only_fields = ['user', 'status', 'merchant_request_id', 'checkout_request_id',
                          'response_code', 'response_description', 'result_code', 'result_description',
                          'mpesa_receipt_number', 'transaction_date', 'created_at', 'updated_at']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        read_only_fields = ['user', 'is_verified', 'created_at', 'updated_at']


class PaymentMethodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['method_type', 'phone_number', 'account_name', 'bank_name', 'account_number']
    
    def validate(self, attrs):
        method_type = attrs.get('method_type')
        
        if method_type == 'mpesa' and not attrs.get('phone_number'):
            raise serializers.ValidationError("Phone number is required for M-Pesa")
        
        if method_type == 'bank' and not all([attrs.get('account_name'), attrs.get('bank_name'), attrs.get('account_number')]):
            raise serializers.ValidationError("Account name, bank name, and account number are required for bank transfer")
        
        return attrs


class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = '__all__'
        read_only_fields = ['created_at']
