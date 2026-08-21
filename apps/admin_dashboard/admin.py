from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class LiamTradersAdminSite(AdminSite):
    site_header = _('Liam Traders Administration')
    site_title = _('Liam Traders Admin')
    index_title = _('Dashboard')
    
    def get_urls(self):
        from django.urls import path
        from django.views.generic import TemplateView
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(TemplateView.as_view(
                template_name='admin/dashboard.html'
            )), name='dashboard'),
        ]
        return custom_urls + urls


# Custom admin site
liam_admin = LiamTradersAdminSite(name='liam_admin')

# Register default models
liam_admin.register(User, UserAdmin)
liam_admin.register(Group, GroupAdmin)

# Register app models
from apps.users.admin import User as CustomUser, Skill, Education, WorkExperience, Notification
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
