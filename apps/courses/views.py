from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from .models import (
    Course, Lesson, Enrollment, LessonProgress, CourseReview,
    Assessment, AssessmentAttempt, InstructorProfile
)
from .serializers import (
    CourseSerializer, CourseCreateSerializer, LessonSerializer,
    EnrollmentSerializer, EnrollmentCreateSerializer, LessonProgressSerializer,
    LessonProgressUpdateSerializer, CourseReviewSerializer,
    AssessmentSerializer, AssessmentAttemptSerializer, InstructorProfileSerializer
)


class CourseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['average_rating', 'number_of_enrollments', 'price', 'created_at']
    
    def get_queryset(self):
        queryset = Course.objects.filter(status='published')
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by price (free or paid)
        is_free = self.request.query_params.get('is_free')
        if is_free:
            queryset = queryset.filter(is_free=is_free == 'true')
        
        # Filter by user's level
        user_level = self.request.user.level
        queryset = queryset.filter(min_level_required__lte=user_level)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseSerializer
    
    def perform_create(self, serializer):
        # Only Level 5 users can create courses
        if self.request.user.level < 5:
            raise permissions.PermissionDenied("You need to be Level 5 to create courses")
        serializer.save(instructor=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CourseCreateSerializer
        return CourseSerializer
    
    def perform_update(self, serializer):
        course = self.get_object()
        if course.instructor != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own courses")
        serializer.save()


class MyCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)
    
    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)
        
        if course.instructor != self.request.user:
            raise permissions.PermissionDenied("You can only add lessons to your own courses")
        
        serializer.save(course=course)
        course.number_of_lessons += 1
        course.save()


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lesson.objects.all()
    
    def perform_update(self, serializer):
        lesson = self.get_object()
        if lesson.course.instructor != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own lessons")
        serializer.save()


class EnrollmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer
    
    def perform_create(self, serializer):
        course = self.context['course']
        user = self.request.user
        
        # Calculate amount
        amount = 0 if course.is_free else course.price
        
        enrollment = Enrollment.objects.create(
            course=course,
            student=user,
            amount_paid=amount,
            is_paid=course.is_free
        )
        
        # Update course enrollment count
        course.number_of_enrollments += 1
        course.save()
        
        return enrollment


class EnrollmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Enrollment.objects.all()
    
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


class CourseEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)
        
        if course.instructor != self.request.user:
            raise permissions.PermissionDenied("You can only view enrollments for your own courses")
        
        return Enrollment.objects.filter(course_id=course_id)


class LessonProgressListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        enrollment_id = self.kwargs['enrollment_id']
        return LessonProgress.objects.filter(enrollment_id=enrollment_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LessonProgressUpdateSerializer
        return LessonProgressSerializer
    
    def perform_create(self, serializer):
        enrollment_id = self.kwargs['enrollment_id']
        enrollment = Enrollment.objects.get(id=enrollment_id)
        lesson_id = self.request.data.get('lesson_id')
        
        if enrollment.student != self.request.user:
            raise permissions.PermissionDenied("You can only track progress for your own enrollments")
        
        lesson = Lesson.objects.get(id=lesson_id)
        
        progress, created = LessonProgress.objects.update_or_create(
            enrollment=enrollment,
            lesson=lesson,
            defaults=serializer.validated_data
        )
        
        # Update enrollment progress
        total_lessons = enrollment.course.lessons.count()
        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).count()
        
        enrollment.progress_percentage = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
        
        if progress.is_completed and lesson.id not in enrollment.lessons_completed:
            enrollment.lessons_completed.append(lesson.id)
        
        # Check if course is completed
        if enrollment.progress_percentage == 100:
            enrollment.status = 'completed'
            from django.utils import timezone
            enrollment.completed_at = timezone.now()
        
        enrollment.save()
        
        return progress


class LessonProgressDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LessonProgress.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LessonProgressUpdateSerializer
        return LessonProgressSerializer
    
    def get_queryset(self):
        return LessonProgress.objects.filter(enrollment__student=self.request.user)


class CourseReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return CourseReview.objects.filter(course_id=course_id)
    
    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)
        
        # Check if user is enrolled
        if not Enrollment.objects.filter(course=course, student=self.request.user).exists():
            raise permissions.PermissionDenied("You must be enrolled in this course to leave a review")
        
        serializer.save(student=self.request.user, course=course)
        
        # Update course rating
        reviews = CourseReview.objects.filter(course=course)
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        course.average_rating = round(avg_rating, 2)
        course.total_reviews = reviews.count()
        course.save()


class AssessmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Assessment.objects.all()


class AssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Assessment.objects.all()


class AssessmentAttemptListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        assessment_id = self.kwargs['assessment_id']
        return AssessmentAttempt.objects.filter(assessment_id=assessment_id, user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AssessmentAttemptSerializer
        return AssessmentAttemptSerializer
    
    def perform_create(self, serializer):
        assessment_id = self.kwargs['assessment_id']
        assessment = Assessment.objects.get(id=assessment_id)
        
        # Check max attempts
        attempts = AssessmentAttempt.objects.filter(
            assessment=assessment,
            user=self.request.user
        ).count()
        
        if attempts >= assessment.max_attempts:
            raise permissions.PermissionDenied("You have reached the maximum number of attempts")
        
        return serializer.save(assessment=assessment, user=self.request.user)


class AssessmentAttemptDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AssessmentAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AssessmentAttempt.objects.all()
    
    def get_queryset(self):
        return AssessmentAttempt.objects.filter(user=self.request.user)


class InstructorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = InstructorProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def course_statistics(request):
    user = request.user
    
    stats = {
        'enrolled_courses': Enrollment.objects.filter(student=user).count(),
        'completed_courses': Enrollment.objects.filter(student=user, status='completed').count(),
        'in_progress_courses': Enrollment.objects.filter(student=user, status='active').count(),
        'total_lessons_completed': LessonProgress.objects.filter(
            enrollment__student=user,
            is_completed=True
        ).count(),
        'assessments_passed': AssessmentAttempt.objects.filter(
            user=user,
            status='passed'
        ).count(),
        'certificates_earned': AssessmentAttempt.objects.filter(
            user=user,
            certificate_issued=True
        ).count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def instructor_statistics(request):
    if request.user.level < 5:
        raise permissions.PermissionDenied("You need to be Level 5 to view instructor statistics")
    
    profile, created = InstructorProfile.objects.get_or_create(user=request.user)
    
    stats = {
        'total_students': profile.total_students,
        'total_courses': profile.total_courses,
        'total_revenue': float(profile.total_revenue),
        'average_rating': float(profile.average_rating),
        'recent_enrollments': EnrollmentSerializer(
            Enrollment.objects.filter(course__instructor=request.user).order_by('-enrolled_at')[:10],
            many=True
        ).data,
    }
    
    return Response(stats)
