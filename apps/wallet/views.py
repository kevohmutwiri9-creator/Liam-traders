from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Q
from .models import Wallet, Transaction, WithdrawalRequest, Earning, BalanceHistory
from .serializers import (
    WalletSerializer, TransactionSerializer, WithdrawalRequestSerializer,
    WithdrawalRequestCreateSerializer, WithdrawalRequestProcessSerializer,
    EarningSerializer, BalanceHistorySerializer
)


class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'reference_id']
    ordering_fields = ['created_at', 'amount']
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class WithdrawalRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WithdrawalRequest.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WithdrawalRequestCreateSerializer
        return WithdrawalRequestSerializer


class WithdrawalRequestDetailView(generics.RetrieveAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = WithdrawalRequest.objects.all()
    
    def get_queryset(self):
        return WithdrawalRequest.objects.filter(user=self.request.user)


class EarningListView(generics.ListAPIView):
    serializer_class = EarningSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at', 'amount']
    
    def get_queryset(self):
        queryset = Earning.objects.filter(user=self.request.user)
        
        # Filter by source
        source = self.request.query_params.get('source')
        if source:
            queryset = queryset.filter(source=source)
        
        # Filter by approval status
        is_approved = self.request.query_params.get('is_approved')
        if is_approved:
            queryset = queryset.filter(is_approved=is_approved == 'true')
        
        return queryset


class EarningDetailView(generics.RetrieveAPIView):
    serializer_class = EarningSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Earning.objects.all()
    
    def get_queryset(self):
        return Earning.objects.filter(user=self.request.user)


class BalanceHistoryView(generics.ListAPIView):
    serializer_class = BalanceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BalanceHistory.objects.filter(user=self.request.user)


class AdminWithdrawalRequestsView(generics.ListAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = WithdrawalRequest.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


class AdminWithdrawalRequestProcessView(generics.UpdateAPIView):
    serializer_class = WithdrawalRequestProcessSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = WithdrawalRequest.objects.all()
    
    def perform_update(self, serializer):
        from django.utils import timezone
        withdrawal = self.get_object()
        
        serializer.save(
            processed_by=self.request.user,
            processed_at=timezone.now()
        )
        
        # If completed, mark transaction as completed
        if serializer.validated_data.get('status') == 'completed':
            transaction = Transaction.objects.filter(withdrawal_request=withdrawal).first()
            if transaction:
                transaction.complete()
        
        # If failed, refund to wallet
        if serializer.validated_data.get('status') == 'failed':
            wallet, created = Wallet.objects.get_or_create(user=withdrawal.user)
            wallet.available_balance += withdrawal.amount
            wallet.save()


class AdminTransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = Transaction.objects.all()
        
        # Filter by type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def wallet_statistics(request):
    user = request.user
    wallet, created = Wallet.objects.get_or_create(user=user)
    
    stats = {
        'pending_balance': float(wallet.pending_balance),
        'available_balance': float(wallet.available_balance),
        'total_earnings': float(wallet.total_earnings),
        'total_withdrawn': float(wallet.total_withdrawn),
        'pending_withdrawals': WithdrawalRequest.objects.filter(
            user=user,
            status__in=['pending', 'processing']
        ).count(),
        'completed_withdrawals': WithdrawalRequest.objects.filter(
            user=user,
            status='completed'
        ).count(),
        'total_transactions': Transaction.objects.filter(user=user).count(),
        'recent_transactions': TransactionSerializer(
            Transaction.objects.filter(user=user)[:10],
            many=True
        ).data,
    }
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_earning(request):
    """Add earning to user's wallet (internal use)"""
    amount = request.data.get('amount')
    source = request.data.get('source', 'task')
    description = request.data.get('description', 'Earning')
    
    if not amount:
        return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Add to pending
    wallet.add_pending(float(amount))
    
    # Create earning record
    earning = Earning.objects.create(
        user=request.user,
        source=source,
        amount=float(amount),
        description=description
    )
    
    # Create transaction
    transaction = Transaction.objects.create(
        user=request.user,
        transaction_type=source if source in ['survey_reward', 'task_payment', 'course_earning'] else 'earning',
        amount=float(amount),
        description=description,
        fee_amount=0,
        net_amount=float(amount)
    )
    
    return Response({
        'message': 'Earning added successfully',
        'earning_id': earning.id,
        'transaction_id': transaction.id,
        'pending_balance': float(wallet.pending_balance)
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_earning(request, earning_id):
    """Approve earning and move to available balance"""
    try:
        earning = Earning.objects.get(id=earning_id)
    except Earning.DoesNotExist:
        return Response({'error': 'Earning not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if earning.is_approved:
        return Response({'error': 'Earning already approved'}, status=status.HTTP_400_BAD_REQUEST)
    
    wallet, created = Wallet.objects.get_or_create(user=earning.user)
    
    if wallet.approve_earnings(earning.amount):
        earning.is_approved = True
        from django.utils import timezone
        earning.approved_at = timezone.now()
        earning.save()
        
        # Update transaction
        transaction = Transaction.objects.filter(
            user=earning.user,
            amount=earning.amount,
            status='pending'
        ).first()
        if transaction:
            transaction.complete()
        
        return Response({'message': 'Earning approved successfully'}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Failed to approve earning'}, status=status.HTTP_400_BAD_REQUEST)
