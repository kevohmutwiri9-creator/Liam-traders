from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.courses.models import Course
from apps.tasks.models import Task
from apps.admin_dashboard.views import LOG_STORAGE
from apps.wallet.models import Wallet

User = get_user_model()


class AdminDashboardApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='StrongPass123!',
            full_name='Admin User',
            is_staff=True,
            is_superuser=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_get_stats_returns_full_analytics_payload(self):
        User.objects.create_user(
            email='member@example.com',
            password='StrongPass123!',
            full_name='Member User',
        )
        Task.objects.create(
            title='Task One',
            description='Sample task',
            task_type='microtask',
            status='open',
            estimated_time_hours=2,
            deadline='2030-01-01T00:00:00Z',
            budget=500,
            client=self.admin,
        )
        Course.objects.create(
            title='Course One',
            description='Sample course',
            category='programming',
            difficulty='beginner',
            status='published',
            instructor=self.admin,
            duration_hours=3,
            slug='course-one',
        )

        response = self.client.get('/api/admin-dashboard/stats/')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('total_users', payload)
        self.assertIn('total_tasks', payload)
        self.assertIn('total_courses', payload)
        self.assertIn('level_distribution', payload)
        self.assertIn('recent_users', payload)

    def test_get_logs_returns_logged_entries(self):
        LOG_STORAGE.clear()
        LOG_STORAGE.append({
            'timestamp': '2026-01-01T00:00:00Z',
            'level': 'INFO',
            'message': 'admin event test',
            'source': 'apps.admin_dashboard.tests',
        })

        response = self.client.get('/api/admin-dashboard/logs/')

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
        self.assertEqual(response.json()[0]['message'], 'admin event test')

    def test_admin_earnings_update_syncs_user_and_wallet(self):
        user = User.objects.create_user(
            email='earning-user@example.com',
            password='StrongPass123!',
            full_name='Earning User',
        )

        response = self.client.patch(
            f'/api/admin-dashboard/users/{user.pk}/',
            {'total_earnings': '425.50'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        wallet = Wallet.objects.get(user=user)
        self.assertEqual(user.total_earnings, 425.50)
        self.assertEqual(user.available_balance, 425.50)
        self.assertEqual(wallet.total_earnings, 425.50)
        self.assertEqual(wallet.available_balance, 425.50)
        self.assertTrue(user.notifications.filter(title='Earnings Updated').exists())
