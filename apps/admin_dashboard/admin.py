from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User as CustomUser
from apps.tasks.models import Task, TaskSubmission
from apps.surveys.models import Survey, SurveyResponse
from apps.courses.models import Course, Enrollment
from apps.wallet.models import Wallet, Transaction, WithdrawalRequest


class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Time ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # User Statistics
        total_users = CustomUser.objects.count()
        new_users_today = CustomUser.objects.filter(created_at__date=today).count()
        new_users_week = CustomUser.objects.filter(created_at__date__gte=week_ago).count()
        new_users_month = CustomUser.objects.filter(created_at__date__gte=month_ago).count()
        
        # Level distribution
        level_distribution = []
        for level_num in range(1, 6):
            count = CustomUser.objects.filter(level=level_num).count()
            level_name = dict(CustomUser.LEVEL_CHOICES).get(level_num, f'Level {level_num}')
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
        recent_users = CustomUser.objects.order_by('-created_at')[:10]
        recent_withdrawals = WithdrawalRequest.objects.order_by('-created_at')[:10]
        recent_transactions = Transaction.objects.order_by('-created_at')[:10]
        
        # Revenue this month
        monthly_revenue = Transaction.objects.filter(
            created_at__date__gte=month_ago,
            transaction_type__in=['earning', 'survey_reward', 'task_payment', 'course_earning']
        ).aggregate(total=Sum('net_amount'))['total'] or 0
        
        # Add all data to context
        context.update({
            'title': 'Dashboard',
            'total_users': total_users,
            'new_users_today': new_users_today,
            'new_users_week': new_users_week,
            'new_users_month': new_users_month,
            'level_distribution': level_distribution,
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'total_submissions': total_submissions,
            'total_surveys': total_surveys,
            'active_surveys': active_surveys,
            'total_responses': total_responses,
            'pending_reviews': pending_reviews,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'completed_enrollments': completed_enrollments,
            'total_wallet_balance': total_wallet_balance,
            'total_pending_balance': total_pending_balance,
            'total_earnings': total_earnings,
            'total_withdrawn': total_withdrawn,
            'pending_withdrawals': pending_withdrawals,
            'monthly_revenue': monthly_revenue,
            'recent_users': recent_users,
            'recent_withdrawals': recent_withdrawals,
            'recent_transactions': recent_transactions,
        })
        
        return context


class LiamTradersAdminSite(AdminSite):
    site_header = _('Liam Traders Administration')
    site_title = _('Liam Traders Admin')
    index_title = _('Dashboard')
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(DashboardView.as_view()), name='dashboard'),
        ]
        return custom_urls + urls


# Custom admin site
liam_admin = LiamTradersAdminSite(name='liam_admin')

# Register default models
liam_admin.register(User, UserAdmin)
liam_admin.register(Group, GroupAdmin)

# Register app models
from apps.users.admin import User as CustomUser, Skill, Education, WorkExperience, Notification, LevelUpgradePayment
from apps.tasks.admin import Task, TaskApplication, TaskSubmission, TaskReview, Milestone
from apps.surveys.admin import Survey, Question, SurveyResponse, SurveyPartner
from apps.courses.admin import Course, Lesson, Enrollment, LessonProgress, CourseReview, Assessment, AssessmentAttempt, InstructorProfile
from apps.wallet.admin import Wallet, Transaction, WithdrawalRequest, Earning, BalanceHistory
from apps.payments.admin import MpesaPayment, PaymentMethod, TransactionLog

liam_admin.register(CustomUser)
liam_admin.register(Skill)
liam_admin.register(Education)
liam_admin.register(WorkExperience)
liam_admin.register(Notification)
liam_admin.register(LevelUpgradePayment)

liam_admin.register(Task)
liam_admin.register(TaskApplication)
liam_admin.register(TaskSubmission)
liam_admin.register(TaskReview)
liam_admin.register(Milestone)

liam_admin.register(Survey)
liam_admin.register(Question)
liam_admin.register(SurveyResponse)
liam_admin.register(SurveyPartner)

liam_admin.register(Course)
liam_admin.register(Lesson)
liam_admin.register(Enrollment)
liam_admin.register(LessonProgress)
liam_admin.register(CourseReview)
liam_admin.register(Assessment)
liam_admin.register(AssessmentAttempt)
liam_admin.register(InstructorProfile)

liam_admin.register(Wallet)
liam_admin.register(Transaction)
liam_admin.register(WithdrawalRequest)
liam_admin.register(Earning)
liam_admin.register(BalanceHistory)

liam_admin.register(MpesaPayment)
liam_admin.register(PaymentMethod)
liam_admin.register(TransactionLog)
