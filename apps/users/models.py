from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    
    LEVEL_CHOICES = [
        (1, 'Starter'),
        (2, 'Worker'),
        (3, 'Professional'),
        (4, 'Expert'),
        (5, 'Academy/Master'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('programming', 'Programming'),
        ('writing', 'Writing'),
        ('design', 'Design'),
        ('data', 'Data Analysis'),
        ('marketing', 'Marketing'),
        ('testing', 'Testing'),
        ('research', 'Research'),
    ]
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Profile Information
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Level System
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    total_tasks_completed = models.IntegerField(default=0)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Specialization
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    
    # Verification
    is_identity_verified = models.BooleanField(default=False)
    identity_document = models.FileField(upload_to='identity_documents/', blank=True, null=True)
    
    # Statistics
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Referral System
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    referral_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_referrals = models.IntegerField(default=0)
    
    # Reputation
    reputation_score = models.IntegerField(default=0)
    positive_reviews = models.IntegerField(default=0)
    negative_reviews = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def can_upgrade_level(self):
        """Check if user meets requirements for next level"""
        from django.conf import settings
        next_level = self.level + 1
        
        if next_level > 5:
            return False
        
        requirements = settings.LEVEL_REQUIREMENTS.get(next_level, {})
        
        if self.total_tasks_completed < requirements.get('required_tasks', 0):
            return False
        
        if self.quality_score < requirements.get('required_quality_score', 0):
            return False
        
        if requirements.get('specialization', False) and not self.specialization:
            return False
        
        return True
    
    def upgrade_level(self):
        """Upgrade user to next level if requirements are met"""
        if self.can_upgrade_level():
            self.level += 1
            self.save()
            return True
        return False
    
    def generate_referral_code(self):
        """Generate a unique referral code for the user"""
        import random
        import string
        if not self.referral_code:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            # Ensure uniqueness
            while User.objects.filter(referral_code=code).exists():
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            self.referral_code = code
            self.save()
        return self.referral_code
    
    def add_referral_earning(self, amount):
        """Add referral earnings to user's balance"""
        self.referral_earnings += amount
        self.available_balance += amount
        self.total_earnings += amount
        self.save()


class Skill(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    years_of_experience = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='skill_certificates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.degree}"


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experience')
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.position} at {self.company}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('task', 'Task'),
        ('payment', 'Payment'),
        ('level', 'Level'),
        ('course', 'Course'),
        ('system', 'System'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
