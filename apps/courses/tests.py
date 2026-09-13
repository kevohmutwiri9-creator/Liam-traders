from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.courses.models import Course, Enrollment, Lesson, LessonNote
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

    def test_student_can_create_and_update_lesson_note(self):
        instructor = User.objects.create_user(
            email='notes-instructor@example.com', password='StrongPass123!',
            full_name='Notes Instructor', is_staff=True,
        )
        student = User.objects.create_user(
            email='notes-student@example.com', password='StrongPass123!',
            full_name='Notes Student',
        )
        course = Course.objects.create(
            title='Notes Course', description='A notes course', category='programming',
            difficulty='beginner', status='published', instructor=instructor,
            duration_hours=1, number_of_lessons=1, slug='notes-course-test',
        )
        lesson = Lesson.objects.create(course=course, title='Lesson One', content='Read this.')

        client = APIClient()
        client.force_authenticate(user=student)
        first = client.post('/api/courses/notes/', {'lesson_id': lesson.pk, 'content': 'First note'}, format='json')
        second = client.post('/api/courses/notes/', {'lesson_id': lesson.pk, 'content': 'Updated note'}, format='json')

        self.assertEqual(first.status_code, 201, first.data)
        self.assertEqual(second.status_code, 201, second.data)
        self.assertEqual(LessonNote.objects.get(user=student, lesson=lesson).content, 'Updated note')