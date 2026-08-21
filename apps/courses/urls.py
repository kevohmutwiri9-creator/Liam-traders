from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, MyCoursesView,
    LessonListCreateView, LessonDetailView,
    EnrollmentListCreateView, EnrollmentDetailView, CourseEnrollmentsView,
    LessonProgressListCreateView, LessonProgressDetailView,
    CourseReviewListCreateView,
    AssessmentListCreateView, AssessmentDetailView,
    AssessmentAttemptListCreateView, AssessmentAttemptDetailView,
    InstructorProfileView, course_statistics, instructor_statistics
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='courses-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='course-lessons'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollments'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('<int:course_id>/enrollments/', CourseEnrollmentsView.as_view(), name='course-enrollments'),
    path('enrollments/<int:enrollment_id>/progress/', LessonProgressListCreateView.as_view(), name='lesson-progress'),
    path('progress/<int:pk>/', LessonProgressDetailView.as_view(), name='progress-detail'),
    path('<int:course_id>/reviews/', CourseReviewListCreateView.as_view(), name='course-reviews'),
    path('assessments/', AssessmentListCreateView.as_view(), name='assessments'),
    path('assessments/<int:pk>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('assessments/<int:assessment_id>/attempts/', AssessmentAttemptListCreateView.as_view(), name='assessment-attempts'),
    path('attempts/<int:pk>/', AssessmentAttemptDetailView.as_view(), name='attempt-detail'),
    path('instructor-profile/', InstructorProfileView.as_view(), name='instructor-profile'),
    path('statistics/', course_statistics, name='course-statistics'),
    path('instructor-statistics/', instructor_statistics, name='instructor-statistics'),
]
