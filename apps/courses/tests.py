from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.courses.models import Course, Enrollment
from apps.users.models import User


class CourseEnrollmentApiTests(TestCase):
    def test_user_can_enroll_in_published_course(self):
        instructor = User.objects.create_user(
            email='instructor@example.com',
            password='StrongPass123!',
            full_name='Course Instructor',
            is_staff=True,
        )
        student = User.objects.create_user(
            email='student@example.com',
            password='StrongPass123!',
            full_name='Course Student',
        )
        course = Course.objects.create(
            title='Published Course',
            description='A published course for testing.',
            category='programming',
            difficulty='beginner',
            status='published',
            instructor=instructor,
            is_free=True,
            price=Decimal('0.00'),
            duration_hours=4,
            number_of_lessons=1,
            slug='published-course-test',
        )

        client = APIClient()
        client.force_authenticate(user=student)
        response = client.post(
            reverse('enrollments'),
            {'course_id': course.pk},
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(Enrollment.objects.filter(course=course, student=student).exists())
        course.refresh_from_db()
        self.assertEqual(course.number_of_enrollments, 1)