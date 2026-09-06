from decimal import Decimal

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.courses.models import CourseTemplate
from apps.seed_content import ensure_demo_content
from apps.surveys.models import QuestionBank, SurveyTemplate
from apps.tasks.models import TaskTemplate
from apps.users.models import LevelUpgradePayment, User
from apps.users.serializers import UserCreateSerializer
from apps.users.views import PaymentApprovalView


class UserCreateSerializerTests(TestCase):
    def test_valid_referral_code_is_accepted_and_saved(self):
        referrer = User.objects.create_user(
            email='kevohmutwiri35@gmail.com',
            password='kevoh2071M@',
            full_name='kelvin Mutwiri',
        )
        referrer.generate_referral_code()

        serializer = UserCreateSerializer(
            data={
                'email': 'kevohmutwiri8@gmail.com',
                'full_name': 'New User',
                'password': 'StrongPass123!',
                're_password': 'StrongPass123!',
                'referral_code': referrer.referral_code,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(user.referred_by, referrer)
        self.assertEqual(user.referral_code, user.referral_code)

    def test_invalid_referral_code_is_ignored(self):
        serializer = UserCreateSerializer(
            data={
                'email': 'newuser2@example.com',
                'full_name': 'New User 2',
                'password': 'StrongPass123!',
                're_password': 'StrongPass123!',
                'referral_code': 'NO_SUCH_CODE',
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertIsNone(user.referred_by)


class MembershipConfigTests(TestCase):
    def test_activation_fee_and_level_range_are_configured(self):
        self.assertEqual(settings.ACTIVATION_FEE, 200)
        self.assertEqual(sorted(settings.LEVEL_REQUIREMENTS.keys()), [1, 2, 3, 4, 5])


class DemoContentSeedTests(TestCase):
    def test_demo_content_is_created_when_missing(self):
        CourseTemplate.objects.all().delete()
        SurveyTemplate.objects.all().delete()
        TaskTemplate.objects.all().delete()
        QuestionBank.objects.all().delete()

        ensure_demo_content()

        self.assertGreater(CourseTemplate.objects.count(), 0)
        self.assertGreater(SurveyTemplate.objects.count(), 0)
        self.assertGreater(TaskTemplate.objects.count(), 0)
        self.assertGreater(QuestionBank.objects.count(), 0)


class PaymentApprovalFlowTests(TestCase):
    def test_admin_approval_creates_notification_and_updates_level(self):
        admin = User.objects.create_user(
            email='admin@example.com',
            password='StrongPass123!',
            full_name='Admin User',
            is_staff=True,
        )
        user = User.objects.create_user(
            email='learner@example.com',
            password='StrongPass123!',
            full_name='Learner User',
            level=1,
        )

        payment = LevelUpgradePayment.objects.create(
            user=user,
            target_level=2,
            amount=Decimal('200.00'),
            transaction_reference='TX-APPROVE-001',
            status='pending',
        )

        factory = APIRequestFactory()
        request = factory.patch(
            f'/api/users/payments/{payment.pk}/approve/',
            {'action': 'approve'},
            format='json',
        )
        force_authenticate(request, user=admin)

        response = PaymentApprovalView.as_view()(request, pk=payment.pk)

        self.assertEqual(response.status_code, 200)
        payment.refresh_from_db()
        user.refresh_from_db()

        self.assertEqual(payment.status, 'approved')
        self.assertEqual(user.level, 2)
        self.assertTrue(user.notifications.filter(title='Level Upgrade Approved').exists())
