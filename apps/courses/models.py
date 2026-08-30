from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import random


class Course(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('web_development', 'Web Development'),
        ('data_science', 'Data Science'),
        ('mobile_development', 'Mobile Development'),
        ('ai_ml', 'AI & Machine Learning'),
        ('cybersecurity', 'Cybersecurity'),
        ('devops', 'DevOps'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Course Details
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructed_courses')
    
    # Pricing
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='KES')
    
    # Requirements
    min_level_required = models.IntegerField(default=1)
    prerequisites = models.JSONField(default=list, blank=True)  # List of course IDs
    required_skills = models.JSONField(default=list, blank=True)
    
    # Course Structure
    duration_hours = models.IntegerField()
    number_of_lessons = models.IntegerField(default=0)
    number_of_enrollments = models.IntegerField(default=0)
    
    # Rating
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    
    # Revenue Sharing
    instructor_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=70.00)  # 70%
    
    # SEO
    slug = models.SlugField(max_length=255, unique=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('coding_exercise', 'Coding Exercise'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='video')
    
    # Content
    video_url = models.URLField(blank=True, null=True)
    video_duration_seconds = models.IntegerField(null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    
    # Resources
    resources = models.JSONField(default=list, blank=True)
    
    # Order
    order = models.IntegerField(default=0)
    
    # Quiz Data (for quiz lessons)
    quiz_data = models.JSONField(default=dict, blank=True)
    
    # Assignment Data (for assignment lessons)
    assignment_instructions = models.TextField(blank=True, null=True)
    assignment_requirements = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Progress
    progress_percentage = models.IntegerField(default=0)
    lessons_completed = models.JSONField(default=list, blank=True)  # List of lesson IDs
    current_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    # Certificate
    certificate_issued = models.BooleanField(default=False)
    certificate_url = models.URLField(blank=True, null=True)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'student']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title}"


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    time_spent_seconds = models.IntegerField(default=0)
    
    # Quiz Results
    quiz_score = models.IntegerField(null=True, blank=True)
    quiz_answers = models.JSONField(default=dict, blank=True)
    
    # Assignment Submission
    assignment_submission = models.TextField(blank=True, null=True)
    assignment_files = models.JSONField(default=list, blank=True)
    assignment_feedback = models.TextField(blank=True, null=True)
    assignment_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['enrollment', 'lesson']
    
    def __str__(self):
        return f"{self.enrollment.student.email} - {self.lesson.title}"


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_reviews')
    
    # Rating
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Detailed Ratings
    content_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    instructor_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    course_structure = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Review
    title = models.CharField(max_length=255)
    comment = models.TextField()
    
    # Helpful votes
    helpful_votes = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title}"


class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ('skill_test', 'Skill Test'),
        ('course_exam', 'Course Exam'),
        ('certification', 'Certification Exam'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    
    # Requirements
    min_level_required = models.IntegerField(default=1)
    required_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments')
    
    # Questions
    questions = models.JSONField(default=list)
    passing_score = models.IntegerField(default=70)  # Percentage
    time_limit_minutes = models.IntegerField()
    
    # Attempts
    max_attempts = models.IntegerField(default=3)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class AssessmentAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    # Results
    score = models.IntegerField(null=True, blank=True)
    answers = models.JSONField(default=dict)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    
    # Certificate (if passed)
    certificate_issued = models.BooleanField(default=False)
    certificate_url = models.URLField(blank=True, null=True)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.assessment.title}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    
    # Instructor Details
    bio = models.TextField()
    expertise = models.JSONField(default=list)
    years_of_experience = models.IntegerField(default=0)
    
    # Social Links
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    
    # Statistics
    total_students = models.IntegerField(default=0)
    total_courses = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_document = models.FileField(upload_to='instructor_verification/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.full_name} - Instructor"


class CourseTemplate(models.Model):
    """Template for auto-generating courses"""
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('web_development', 'Web Development'),
        ('data_science', 'Data Science'),
        ('mobile_development', 'Mobile Development'),
        ('ai_ml', 'AI & Machine Learning'),
        ('cybersecurity', 'Cybersecurity'),
        ('devops', 'DevOps'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    description = models.TextField()
    
    # Course Configuration
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.IntegerField()
    number_of_lessons = models.IntegerField(default=10)
    
    # Requirements
    min_level_required = models.IntegerField(default=1)
    required_skills = models.JSONField(default=list, blank=True)
    
    # Auto-generation settings
    auto_generate = models.BooleanField(default=False)
    generate_frequency_hours = models.IntegerField(default=168)  # Weekly by default
    max_active_courses = models.IntegerField(default=5)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def generate_course(self):
        """Generate a new course from this template"""
        from django.utils import timezone
        from datetime import timedelta
        from django.contrib.auth import get_user_model
        from django.utils.text import slugify
        
        User = get_user_model()
        
        # Check if we've reached max active courses
        active_count = Course.objects.filter(
            status='published',
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        if active_count >= self.max_active_courses:
            return None
        
        # Get a random instructor (or use system user)
        try:
            instructor = User.objects.filter(is_staff=True).first()
        except:
            instructor = None
        
        # Create course
        import uuid
        unique_suffix = str(uuid.uuid4())[:8]
        course = Course.objects.create(
            title=f"{self.name} - {timezone.now().strftime('%B %Y')}",
            description=self.description,
            category=self.category,
            difficulty=self.difficulty,
            status='published',
            instructor=instructor,
            is_free=self.base_price == 0,
            price=self.base_price,
            min_level_required=self.min_level_required,
            required_skills=self.required_skills,
            duration_hours=self.duration_hours,
            number_of_lessons=self.number_of_lessons,
            slug=slugify(f"{self.name}-{timezone.now().strftime('%B-%Y')}-{unique_suffix}"),
            published_at=timezone.now()
        )
        
        # Generate lessons
        lesson_titles = [
            "Introduction to the Course",
            "Getting Started",
            "Core Concepts",
            "Practical Examples",
            "Advanced Techniques",
            "Best Practices",
            "Real-world Applications",
            "Troubleshooting",
            "Project Work",
            "Final Assessment"
        ]
        
        for idx, title in enumerate(lesson_titles[:self.number_of_lessons]):
            Lesson.objects.create(
                course=course,
                title=title,
                description=f"Learn about {title}",
                lesson_type='video',
                order=idx + 1,
                video_duration_seconds=random.randint(600, 3600)  # 10-60 minutes
            )
        
        return course
