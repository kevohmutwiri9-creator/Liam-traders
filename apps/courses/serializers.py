from rest_framework import serializers
from .models import (
    Course, Lesson, Enrollment, LessonProgress, CourseReview,
    Assessment, AssessmentAttempt, InstructorProfile
)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['course', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.full_name', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'number_of_enrollments', 'average_rating', 
                          'total_reviews', 'created_at', 'updated_at', 'published_at']


class CourseCreateSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'number_of_enrollments', 'average_rating',
                          'total_reviews', 'created_at', 'updated_at', 'published_at']
    
    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])
        course = Course.objects.create(**validated_data)
        
        for lesson_data in lessons_data:
            Lesson.objects.create(course=course, **lesson_data)
        
        course.number_of_lessons = len(lessons_data)
        course.save()
        
        return course


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['student', 'progress_percentage', 'lessons_completed',
                          'enrolled_at', 'completed_at', 'last_accessed_at']


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = '__all__'
        read_only_fields = ['enrollment']


class CourseReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = '__all__'
        read_only_fields = ['student', 'helpful_votes', 'created_at', 'updated_at']


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentAttempt
        fields = '__all__'
        read_only_fields = ['user', 'status', 'score', 'certificate_issued',
                          'certificate_url', 'started_at', 'completed_at']


class InstructorProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        read_only_fields = ['user', 'total_students', 'total_courses', 'total_revenue',
                          'average_rating', 'created_at', 'updated_at']


class EnrollmentCreateSerializer(serializers.Serializer):
    def validate(self, attrs):
        course = self.context['course']
        user = self.context['request'].user
        
        # Check if already enrolled
        if Enrollment.objects.filter(course=course, student=user).exists():
            raise serializers.ValidationError("You are already enrolled in this course")
        
        # Check if course is published
        if course.status != 'published':
            raise serializers.ValidationError("This course is not available for enrollment")
        
        # Check if user meets level requirement
        if user.level < course.min_level_required:
            raise serializers.ValidationError(
                f"You need to be at least Level {course.min_level_required} to enroll in this course"
            )
        
        # Check prerequisites
        if course.prerequisites:
            enrolled_prerequisites = Enrollment.objects.filter(
                course_id__in=course.prerequisites,
                student=user,
                status='completed'
            ).count()
            
            if enrolled_prerequisites < len(course.prerequisites):
                raise serializers.ValidationError("You must complete the prerequisite courses first")
        
        return attrs


class LessonProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['is_completed', 'time_spent_seconds', 'quiz_score', 'quiz_answers',
                  'assignment_submission', 'assignment_files']
