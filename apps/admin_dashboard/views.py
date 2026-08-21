from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
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
