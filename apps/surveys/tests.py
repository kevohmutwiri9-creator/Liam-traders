from datetime import timedelta

from django.test import TestCase
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
