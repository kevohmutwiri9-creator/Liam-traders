from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from apps.users.models import User
from apps.tasks.models import Task, TaskApplication


class TaskApplicationApiTests(TestCase):
    def test_worker_can_apply_to_open_task(self):
        client = User.objects.create_user(
            email='client@example.com',
            password='StrongPass123!',
            full_name='Task Client',
            is_staff=True,
        )
        worker = User.objects.create_user(
            email='worker@example.com',
            password='StrongPass123!',
            full_name='Task Worker',
        )
        task = Task.objects.create(
            title='Test task',
            description='A task for API testing.',
            task_type='data_entry',
            status='open',
            priority='medium',
            estimated_time_hours=Decimal('2.00'),
            deadline=timezone.now() + timedelta(days=2),
            budget=Decimal('150.00'),
            client=client,
        )

        api_client = APIClient()
        api_client.force_authenticate(user=worker)
        response = api_client.post(
            reverse('task-applications', kwargs={'task_id': task.pk}),
            {
                'cover_letter': 'I can complete this task carefully.',
                'proposed_amount': '150.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(TaskApplication.objects.filter(task=task, worker=worker).exists())