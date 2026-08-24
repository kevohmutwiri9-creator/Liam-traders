from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import random


class Survey(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    
    CATEGORY_CHOICES = [
        ('market_research', 'Market Research'),
        ('product_feedback', 'Product Feedback'),
        ('customer_satisfaction', 'Customer Satisfaction'),
        ('academic', 'Academic'),
        ('opinion', 'Opinion'),
        ('lifestyle', 'Lifestyle'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Survey Details
    estimated_time_minutes = models.IntegerField()
    number_of_questions = models.IntegerField(default=0)
    max_participants = models.IntegerField()
    current_participants = models.IntegerField(default=0)
    
    # Payment
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Requirements
    min_level_required = models.IntegerField(default=1)
    required_specializations = models.JSONField(default=list, blank=True)
    target_demographics = models.JSONField(default=dict, blank=True)
    
    # Partner Information
    partner_name = models.CharField(max_length=255, blank=True, null=True)
    partner_company = models.CharField(max_length=255, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date and
            self.current_participants < self.max_participants
        )


class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('multiple_choice', 'Multiple Choice'),
        ('checkbox', 'Checkbox'),
        ('rating', 'Rating'),
        ('dropdown', 'Dropdown'),
        ('date', 'Date'),
        ('number', 'Number'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)
    options = models.JSONField(default=list, blank=True)  # For multiple choice, checkbox, dropdown
    min_value = models.IntegerField(null=True, blank=True)  # For rating, number
    max_value = models.IntegerField(null=True, blank=True)  # For rating, number
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.survey.title} - Q{self.order}"


class SurveyResponse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_responses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    answers = models.JSONField(default=dict)
    completion_time_seconds = models.IntegerField()
    
    # Quality Check
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_surveys'
    )
    review_notes = models.TextField(blank=True, null=True)
    
    # Payment
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['survey', 'user']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.survey.title}"


class SurveyPartner(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # Percentage
    total_surveys = models.IntegerField(default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.company


class SurveyTemplate(models.Model):
    """Template for auto-generating surveys"""
    CATEGORY_CHOICES = [
        ('market_research', 'Market Research'),
        ('product_feedback', 'Product Feedback'),
        ('customer_satisfaction', 'Customer Satisfaction'),
        ('academic', 'Academic'),
        ('opinion', 'Opinion'),
        ('lifestyle', 'Lifestyle'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    # Survey Configuration
    base_reward_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_time_minutes = models.IntegerField()
    max_participants = models.IntegerField()
    
    # Auto-generation settings
    auto_generate = models.BooleanField(default=False)
    generate_frequency_hours = models.IntegerField(default=24)  # How often to generate
    max_active_surveys = models.IntegerField(default=5)  # Max active surveys from this template
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def generate_survey(self):
        """Generate a new survey from this template"""
        from django.utils import timezone
        from datetime import timedelta
        
        # Check if we've reached max active surveys
        active_count = Survey.objects.filter(
            status='active',
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        if active_count >= self.max_active_surveys:
            return None
        
        # Create survey
        survey = Survey.objects.create(
            title=f"{self.name} - {timezone.now().strftime('%B %d, %Y')}",
            description=self.description,
            category=self.category,
            status='active',
            estimated_time_minutes=self.estimated_time_minutes,
            max_participants=self.max_participants,
            reward_amount=self.base_reward_amount,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
        )
        
        # Generate questions from question bank
        questions = QuestionBank.objects.filter(category=self.category)
        selected_questions = random.sample(list(questions), min(len(questions), 10))
        
        for idx, qb in enumerate(selected_questions):
            Question.objects.create(
                survey=survey,
                question_text=qb.question_text,
                question_type=qb.question_type,
                order=idx + 1,
                options=qb.options,
                min_value=qb.min_value,
                max_value=qb.max_value
            )
        
        survey.number_of_questions = len(selected_questions)
        survey.save()
        
        return survey


class QuestionBank(models.Model):
    """Bank of questions for auto-generating surveys"""
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('multiple_choice', 'Multiple Choice'),
        ('checkbox', 'Checkbox'),
        ('rating', 'Rating'),
        ('dropdown', 'Dropdown'),
        ('date', 'Date'),
        ('number', 'Number'),
    ]
    
    CATEGORY_CHOICES = [
        ('market_research', 'Market Research'),
        ('product_feedback', 'Product Feedback'),
        ('customer_satisfaction', 'Customer Satisfaction'),
        ('academic', 'Academic'),
        ('opinion', 'Opinion'),
        ('lifestyle', 'Lifestyle'),
    ]
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    options = models.JSONField(default=list, blank=True)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'id']
    
    def __str__(self):
        return f"{self.category} - {self.question_text[:50]}"
