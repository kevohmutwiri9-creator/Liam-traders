from django.urls import path
from .views import (
    WalletView, TransactionListView, TransactionDetailView,
    WithdrawalRequestListCreateView, WithdrawalRequestDetailView,
    EarningListView, EarningDetailView, BalanceHistoryView,
    AdminWithdrawalRequestsView, AdminWithdrawalRequestProcessView,
    AdminTransactionsView, wallet_statistics, add_earning, approve_earning
)

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('withdrawals/', WithdrawalRequestListCreateView.as_view(), name='withdrawals'),
    path('withdrawals/<int:pk>/', WithdrawalRequestDetailView.as_view(), name='withdrawal-detail'),
    path('earnings/', EarningListView.as_view(), name='earnings'),
    path('earnings/<int:pk>/', EarningDetailView.as_view(), name='earning-detail'),
    path('history/', BalanceHistoryView.as_view(), name='balance-history'),
    path('statistics/', wallet_statistics, name='wallet-statistics'),
    path('add-earning/', add_earning, name='add-earning'),
    path('admin/withdrawals/', AdminWithdrawalRequestsView.as_view(), name='admin-withdrawals'),
    path('admin/withdrawals/<int:pk>/process/', AdminWithdrawalRequestProcessView.as_view(), name='admin-process-withdrawal'),
    path('admin/transactions/', AdminTransactionsView.as_view(), name='admin-transactions'),
    path('admin/earnings/<int:earning_id>/approve/', approve_earning, name='approve-earning'),
]
