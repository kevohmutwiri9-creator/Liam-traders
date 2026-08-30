from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from apps.users.models import User
from apps.tasks.models import Task, TaskSubmission
from apps.surveys.models import Survey, SurveyResponse
from apps.courses.models import Course, Enrollment
from apps.wallet.models import Wallet, Transaction, WithdrawalRequest
from apps.payments.models import MpesaPayment


@staff_member_required
def dashboard(request):
    # Time ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # User Statistics
    total_users = User.objects.count()
    new_users_today = User.objects.filter(created_at__date=today).count()
    new_users_week = User.objects.filter(created_at__date__gte=week_ago).count()
    new_users_month = User.objects.filter(created_at__date__gte=month_ago).count()
    
    # Level distribution
    level_distribution = []
    for level_num in range(1, 6):
        count = User.objects.filter(level=level_num).count()
        level_name = dict(User.LEVEL_CHOICES).get(level_num)
        level_distribution.append({'level': level_name, 'count': count})
    
    # Task Statistics
    total_tasks = Task.objects.count()
    active_tasks = Task.objects.filter(status='open').count()
    completed_tasks = Task.objects.filter(status='completed').count()
    total_submissions = TaskSubmission.objects.count()
    
    # Survey Statistics
    total_surveys = Survey.objects.count()
    active_surveys = Survey.objects.filter(status='active').count()
    total_responses = SurveyResponse.objects.count()
    pending_reviews = SurveyResponse.objects.filter(status='pending').count()
    
    # Course Statistics
    total_courses = Course.objects.filter(status='published').count()
    total_enrollments = Enrollment.objects.count()
    completed_enrollments = Enrollment.objects.filter(status='completed').count()
    
    # Financial Statistics
    total_wallet_balance = Wallet.objects.aggregate(
        total=Sum('available_balance')
    )['total'] or 0
    
    total_pending_balance = Wallet.objects.aggregate(
        total=Sum('pending_balance')
    )['total'] or 0
    
    total_earnings = Wallet.objects.aggregate(
        total=Sum('total_earnings')
    )['total'] or 0
    
    total_withdrawn = Wallet.objects.aggregate(
        total=Sum('total_withdrawn')
    )['total'] or 0
    
    pending_withdrawals = WithdrawalRequest.objects.filter(
        status__in=['pending', 'processing']
    ).count()
    
    # Recent activity
    recent_users = User.objects.order_by('-created_at')[:10]
    recent_withdrawals = WithdrawalRequest.objects.order_by('-created_at')[:10]
    recent_transactions = Transaction.objects.order_by('-created_at')[:10]
    
    # Revenue this month
    monthly_revenue = Transaction.objects.filter(
        created_at__date__gte=month_ago,
        transaction_type__in=['earning', 'survey_reward', 'task_payment', 'course_earning']
    ).aggregate(total=Sum('net_amount'))['total'] or 0
    
    context = {
        'title': 'Dashboard',
        
        # User Stats
        'total_users': total_users,
        'new_users_today': new_users_today,
        'new_users_week': new_users_week,
        'new_users_month': new_users_month,
        'level_distribution': level_distribution,
        
        # Task Stats
        'total_tasks': total_tasks,
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'total_submissions': total_submissions,
        
        # Survey Stats
        'total_surveys': total_surveys,
        'active_surveys': active_surveys,
        'total_responses': total_responses,
        'pending_reviews': pending_reviews,
        
        # Course Stats
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'completed_enrollments': completed_enrollments,
        
        # Financial Stats
        'total_wallet_balance': total_wallet_balance,
        'total_pending_balance': total_pending_balance,
        'total_earnings': total_earnings,
        'total_withdrawn': total_withdrawn,
        'pending_withdrawals': pending_withdrawals,
        'monthly_revenue': monthly_revenue,
        
        # Recent Activity
        'recent_users': recent_users,
        'recent_withdrawals': recent_withdrawals,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'admin/dashboard.html', context)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    """Get all users for admin management"""
    users = User.objects.all().order_by('-created_at')
    data = []
    
    for user in users:
        data.append({
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'level': user.level,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'total_tasks_completed': user.total_tasks_completed,
            'quality_score': float(user.quality_score) if user.quality_score else 0.0,
            'total_referrals': user.total_referrals,
            'created_at': user.created_at.isoformat(),
        })
    
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_user(request, user_id):
    """Update user information (admin only)"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    if 'level' in request.data:
        user.level = request.data['level']
        # Send notification to user
        from apps.users.models import Notification
        Notification.objects.create(
            user=user,
            title='Level Updated',
            message=f'Your level has been updated to Level {user.level}',
            notification_type='level_upgrade',
            is_read=False
        )
    
    if 'is_active' in request.data:
        user.is_active = request.data['is_active']
    
    user.save()
    
    return Response({'message': 'User updated successfully'})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def ban_user(request, user_id):
    """Ban a user (admin only)"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    user.is_active = False
    user.save()
    
    # Send notification to user
    from apps.users.models import Notification
    Notification.objects.create(
        user=user,
        title='Account Banned',
        message='Your account has been banned. Please contact support for more information.',
        notification_type='account',
        is_read=False
    )
    
    return Response({'message': 'User banned successfully'})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def unban_user(request, user_id):
    """Unban a user (admin only)"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    user.is_active = True
    user.save()
    
    # Send notification to user
    from apps.users.models import Notification
    Notification.objects.create(
        user=user,
        title='Account Reactivated',
        message='Your account has been reactivated. You can now access your account.',
        notification_type='account',
        is_read=False
    )
    
    return Response({'message': 'User unbanned successfully'})
