from django.contrib import admin
from .models import Task, TaskApplication, TaskSubmission, TaskReview, Milestone


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0
    ordering = ['order']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_type', 'status', 'priority', 'budget', 'client', 'assigned_to', 'deadline']
    list_filter = ['status', 'priority', 'task_type', 'min_level_required']
    search_fields = ['title', 'description', 'client__email']
    inlines = [MilestoneInline]
    readonly_fields = ['total_applications', 'views_count', 'created_at', 'updated_at']


@admin.register(TaskApplication)
class TaskApplicationAdmin(admin.ModelAdmin):
    list_display = ['task', 'worker', 'status', 'proposed_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['task__title', 'worker__email']


@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ['task', 'worker', 'status', 'amount_earned', 'is_paid', 'submitted_at']
    list_filter = ['status', 'is_paid', 'submitted_at']
    search_fields = ['task__title', 'worker__email']
    readonly_fields = ['submitted_at', 'reviewed_at']


@admin.register(TaskReview)
class TaskReviewAdmin(admin.ModelAdmin):
    list_display = ['submission', 'reviewer', 'worker', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__email', 'worker__email']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['task', 'title', 'status', 'amount', 'is_paid', 'due_date']
    list_filter = ['status', 'is_paid']
    search_fields = ['task__title', 'title']
