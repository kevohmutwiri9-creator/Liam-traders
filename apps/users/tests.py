from django.test import TestCase

from apps.users.models import User
from apps.users.serializers import UserCreateSerializer


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
