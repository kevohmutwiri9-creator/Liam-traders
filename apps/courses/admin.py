from django.contrib import admin
from .models import (
    Course, Lesson, Enrollment, LessonProgress, CourseReview,
    Assessment, AssessmentAttempt, InstructorProfile
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'status', 'instructor', 'price', 'is_free', 'number_of_enrollments', 'average_rating']
    list_filter = ['status', 'category', 'difficulty', 'is_free']
    search_fields = ['title', 'description', 'instructor__email']
    inlines = [LessonInline]
    readonly_fields = ['number_of_enrollments', 'average_rating', 'total_reviews', 'created_at', 'updated_at']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'lesson_type', 'order', 'video_duration_seconds']
    list_filter = ['lesson_type']
    search_fields = ['title', 'course__title']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'status', 'progress_percentage', 'is_paid', 'enrolled_at']
    list_filter = ['status', 'is_paid', 'enrolled_at']
    search_fields = ['course__title', 'student__email']
    readonly_fields = ['enrolled_at', 'completed_at', 'last_accessed_at']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'quiz_score', 'assignment_grade']
    list_filter = ['is_completed']
    search_fields = ['enrollment__student__email', 'lesson__title']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'rating', 'helpful_votes', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['course__title', 'student__email', 'title']


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'assessment_type', 'min_level_required', 'passing_score', 'time_limit_minutes']
    list_filter = ['assessment_type']
    search_fields = ['title', 'description']


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'user', 'status', 'score', 'certificate_issued', 'started_at']
    list_filter = ['status', 'certificate_issued']
    search_fields = ['assessment__title', 'user__email']


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'total_students', 'total_courses', 'total_revenue', 'average_rating']
    list_filter = ['is_verified']
    search_fields = ['user__email', 'user__full_name']
