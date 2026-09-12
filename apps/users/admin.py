from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Skill, Education, WorkExperience, Notification, LevelUpgradePayment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'level', 'total_tasks_completed', 'quality_score', 'is_identity_verified']
    list_filter = ['level', 'is_identity_verified', 'is_staff', 'is_superuser']
    search_fields = ['email', 'full_name', 'phone_number']
    ordering = ['-created_at']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        financial_fields = {
            'total_earnings', 'available_balance', 'pending_balance'
        }
        if financial_fields.intersection(form.changed_data):
            from apps.wallet.models import Wallet

            wallet, _ = Wallet.objects.get_or_create(user=obj)
            wallet.total_earnings = obj.total_earnings
            wallet.available_balance = obj.available_balance
            wallet.pending_balance = obj.pending_balance
            wallet.save(update_fields=[
                'total_earnings', 'available_balance', 'pending_balance', 'updated_at'
            ])

        if not change:
            return

        changed_fields = [
            field for field in form.changed_data
            if field not in {'updated_at'}
        ]
        if changed_fields:
            Notification.objects.create(
                user=obj,
                type='system',
                title='Account Updated',
                message=(
                    f'An administrator updated your account: '
                    f'{", ".join(changed_fields)}.'
                ),
                notification_type='admin_update',
                action_url='/dashboard/settings',
            )

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('full_name', 'phone_number', 'profile_picture', 'bio', 'location')
        }),
        ('Level System', {
            'fields': ('level', 'total_tasks_completed', 'quality_score', 'specialization', 'skills')
        }),
        ('Verification', {
            'fields': ('is_identity_verified', 'identity_document')
        }),
        ('Financial', {
            'fields': ('total_earnings', 'available_balance', 'pending_balance')
        }),
        ('Reputation', {
            'fields': ('reputation_score', 'positive_reviews', 'negative_reviews')
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'level', 'verified', 'years_of_experience']
    list_filter = ['level', 'verified']
    search_fields = ['name', 'user__email']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'degree', 'field_of_study', 'is_current']
    search_fields = ['institution', 'degree', 'user__email']


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'position', 'is_current']
    search_fields = ['company', 'position', 'user__email']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'title', 'is_read', 'created_at']
    list_filter = ['type', 'is_read']
    search_fields = ['title', 'user__email']


@admin.register(LevelUpgradePayment)
class LevelUpgradePaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_type', 'target_level', 'amount', 'transaction_reference', 'status', 'created_at']
    list_filter = ['payment_type', 'status', 'target_level', 'created_at']
    search_fields = ['user__email', 'user__full_name', 'transaction_reference']
    readonly_fields = ['created_at', 'updated_at', 'processed_at']
    fieldsets = (
        (None, {'fields': ('user', 'payment_type', 'target_level', 'amount', 'transaction_reference', 'status')}),
        ('Admin review', {'fields': ('admin_notes', 'processed_by', 'processed_at')}),
    )

    def save_model(self, request, obj, form, change):
        previous = LevelUpgradePayment.objects.get(pk=obj.pk) if change else None
        if change and previous.status == 'pending' and obj.status == 'approved':
            obj.status = 'pending'
            obj.approve(request.user)
            return
        if change and previous.status == 'pending' and obj.status == 'rejected':
            obj.status = 'pending'
            obj.reject(request.user, obj.admin_notes or '')
            return
        super().save_model(request, obj, form, change)
