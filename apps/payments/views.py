from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from .models import MpesaPayment, PaymentMethod, TransactionLog
from .serializers import (
    MpesaPaymentSerializer, PaymentMethodSerializer,
    PaymentMethodCreateSerializer, TransactionLogSerializer
)
from .mpesa import MpesaAPI
import uuid


class MpesaPaymentListView(generics.ListAPIView):
    serializer_class = MpesaPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MpesaPayment.objects.filter(user=self.request.user)


class MpesaPaymentDetailView(generics.RetrieveAPIView):
    serializer_class = MpesaPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MpesaPayment.objects.all()
    
    def get_queryset(self):
        return MpesaPayment.objects.filter(user=self.request.user)


class PaymentMethodListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PaymentMethod.objects.all()
    
    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_withdrawal(request):
    """Initiate M-Pesa withdrawal"""
    phone_number = request.data.get('phone_number')
    amount = request.data.get('amount')
    
    if not phone_number or not amount:
        return Response(
            {'error': 'Phone number and amount are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user has sufficient balance
    from apps.wallet.models import Wallet
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    if wallet.available_balance < float(amount):
        return Response(
            {'error': 'Insufficient balance'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        mpesa = MpesaAPI()
        
        # Generate unique merchant request ID
        merchant_request_id = str(uuid.uuid4())
        
        # Callback URL (should be configured in production)
        callback_url = f"{settings.BASE_URL}/api/payments/mpesa/callback/"
        
        # Initiate B2C payment
        response = mpesa.initiate_b2c_payment(
            phone_number=phone_number,
            amount=int(amount),
            callback_url=callback_url
        )
        
        # Create M-Pesa payment record
        mpesa_payment = MpesaPayment.objects.create(
            user=request.user,
            transaction_type='withdrawal',
            amount=float(amount),
            phone_number=phone_number,
            merchant_request_id=merchant_request_id,
            checkout_request_id=response.get('ConversationID'),
            response_code=response.get('ResponseCode'),
            response_description=response.get('ResponseDescription')
        )
        
        # Log the transaction
        TransactionLog.objects.create(
            user=request.user,
            endpoint=f"{mpesa.base_url}/mpesa/b2c/v1/paymentrequest",
            method='POST',
            request_data={'phone_number': phone_number, 'amount': amount},
            response_data=response,
            status_code=200,
            success=response.get('ResponseCode') == '0'
        )
        
        return Response({
            'message': 'Withdrawal initiated successfully',
            'payment_id': mpesa_payment.id,
            'merchant_request_id': merchant_request_id,
            'response': response
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([])
def mpesa_callback(request):
    """Handle M-Pesa callback"""
    data = request.data
    
    # Extract callback data
    result = data.get('Result', {})
    result_code = result.get('ResultCode')
    result_description = result.get('ResultDescription')
    merchant_request_id = result.get('MerchantRequestID')
    
    try:
        # Find the payment record
        mpesa_payment = MpesaPayment.objects.get(merchant_request_id=merchant_request_id)
        
        # Update payment status
        mpesa_payment.result_code = result_code
        mpesa_payment.result_description = result_description
        
        if result_code == '0':
            mpesa_payment.status = 'completed'
            mpesa_payment.mpesa_receipt_number = result.get('Result', {}).get('M-PesaReceiptNumber')
            
            # Update withdrawal request if exists
            if mpesa_payment.withdrawal_request:
                from apps.wallet.models import WithdrawalRequest
                withdrawal = mpesa_payment.withdrawal_request
                withdrawal.status = 'completed'
                withdrawal.transaction_id = mpesa_payment.mpesa_receipt_number
                withdrawal.save()
        else:
            mpesa_payment.status = 'failed'
            
            # Refund if withdrawal failed
            if mpesa_payment.withdrawal_request:
                from apps.wallet.models import Wallet, WithdrawalRequest
                wallet, created = Wallet.objects.get_or_create(user=mpesa_payment.user)
                wallet.available_balance += mpesa_payment.amount
                wallet.save()
                
                withdrawal = mpesa_payment.withdrawal_request
                withdrawal.status = 'failed'
                withdrawal.rejection_reason = result_description
                withdrawal.save()
        
        mpesa_payment.save()
        
        return Response({'ResultCode': 0, 'ResultDesc': 'Success'})
        
    except MpesaPayment.DoesNotExist:
        return Response({'ResultCode': 1, 'ResultDesc': 'Payment not found'}, status=404)
    except Exception as e:
        return Response({'ResultCode': 1, 'ResultDesc': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_methods(request):
    """Get user's payment methods"""
    methods = PaymentMethod.objects.filter(user=request.user)
    serializer = PaymentMethodSerializer(methods, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def transaction_logs(request):
    """View transaction logs (admin only)"""
    logs = TransactionLog.objects.all()
    
    # Filter by user
    user_id = request.query_params.get('user_id')
    if user_id:
        logs = logs.filter(user_id=user_id)
    
    # Filter by success
    success = request.query_params.get('success')
    if success:
        logs = logs.filter(success=success == 'true')
    
    serializer = TransactionLogSerializer(logs, many=True)
    return Response(serializer.data)
