from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    TASK_TYPES = [
        ('microtask', 'Microtask'),
        ('data_entry', 'Data Entry'),
        ('transcription', 'Transcription'),
        ('data_labeling', 'Data Labeling'),
        ('ai_evaluation', 'AI Evaluation'),
        ('research', 'Research'),
        ('testing', 'Testing'),
        ('content_creation', 'Content Creation'),
        ('freelance', 'Freelance Project'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Task Details
    estimated_time_hours = models.DecimalField(max_digits=5, decimal_places=2)
    deadline = models.DateTimeField()
    
    # Payment
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_type = models.CharField(max_length=20, choices=[('fixed', 'Fixed'), ('hourly', 'Hourly')], default='fixed')
    
    # Requirements
    min_level_required = models.IntegerField(default=1)
    required_specializations = models.JSONField(default=list, blank=True)
    required_skills = models.JSONField(default=list, blank=True)
    
    # Client Information
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_tasks')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks'
    )
    
    # Attachments
    attachments = models.JSONField(default=list, blank=True)
    
    # Statistics
    total_applications = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TaskApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Application Details
    cover_letter = models.TextField()
    proposed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_completion = models.DateTimeField(null=True, blank=True)
    
    # Attachments
    attachments = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['task', 'worker']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.worker.email} - {self.task.title}"


class TaskSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revision_required', 'Revision Required'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_submissions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    # Submission Details
    description = models.TextField()
    work_files = models.JSONField(default=list)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Payment
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    # Review
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    client_feedback = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_submissions'
    )
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.worker.email} - {self.task.title}"


class TaskReview(models.Model):
    submission = models.OneToOneField(TaskSubmission, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    
    # Rating
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Review Details
    communication = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    timeliness = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    comment = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['submission', 'reviewer']
    
    def __str__(self):
        return f"Review for {self.worker.email}"


class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    # Dates
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Order
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.task.title} - {self.title}"
