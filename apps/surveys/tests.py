from datetime import timedelta

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient

from apps.surveys.models import Survey, SurveyResponse
from apps.users.models import User
from apps.wallet.models import Transaction, Wallet


class SurveyRewardSettlementTests(TestCase):
    def test_approving_response_credits_pending_wallet(self):
        admin = User.objects.create_user(
            email='survey-admin@example.com', password='StrongPass123!',
            full_name='Survey Admin', is_staff=True,
        )
        worker = User.objects.create_user(
            email='survey-worker@example.com', password='StrongPass123!',
            full_name='Survey Worker',
        )
        survey = Survey.objects.create(
            title='Reward Survey', description='Test survey', category='opinion',
            status='active', estimated_time_minutes=5, max_participants=10,
            reward_amount=Decimal('75.00'), start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
        )
        response = SurveyResponse.objects.create(
            survey=survey, user=worker, answers={}, completion_time_seconds=60,
            reward_amount=Decimal('75.00'),
        )

        client = APIClient()
        client.force_authenticate(user=admin)
        result = client.patch(
            reverse('admin-review-response', kwargs={'pk': response.pk}),
            {'status': 'approved', 'quality_score': '90.00'},
            format='json',
        )

        self.assertEqual(result.status_code, 200, result.data)
        wallet = Wallet.objects.get(user=worker)
        self.assertEqual(wallet.pending_balance, Decimal('75.00'))
        worker.refresh_from_db()
        self.assertEqual(worker.pending_balance, Decimal('75.00'))
        self.assertTrue(Transaction.objects.filter(user=worker, transaction_type='survey_reward').exists())
from django.utils import timezone
from rest_framework.test import APIClient

from apps.surveys.models import Question, Survey
from apps.users.models import User


class SurveyQuestionsApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='survey-user@example.com',
            password='StrongPass123!',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        now = timezone.now()
        self.survey = Survey.objects.create(
            title='Test Survey',
            description='A survey for testing',
            category='opinion',
            status='active',
            estimated_time_minutes=5,
            max_participants=100,
            reward_amount=10,
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1),
        )
        Question.objects.create(
            survey=self.survey,
            question_text='What do you think?',
            question_type='text',
            order=1,
        )

    def test_questions_endpoint_returns_paginated_results(self):
        response = self.client.get(f'/api/surveys/{self.survey.id}/questions/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        self.assertEqual(len(response.json()['results']), 1)

    def test_submit_survey_accepts_completion_time(self):
        response = self.client.post(
            f'/api/surveys/{self.survey.id}/submit/',
            {
                'answers': {'1': 'It is useful'},
                'completion_time_seconds': 45,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'Survey submitted successfully')
