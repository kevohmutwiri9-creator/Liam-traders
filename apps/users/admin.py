from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Skill, Education, WorkExperience, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'level', 'total_tasks_completed', 'quality_score', 'is_identity_verified']
    list_filter = ['level', 'is_identity_verified', 'is_staff', 'is_superuser']
    search_fields = ['email', 'full_name', 'phone_number']
    ordering = ['-created_at']
    
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
