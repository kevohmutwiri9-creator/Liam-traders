from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin user from environment variables if it does not exist'

    def handle(self, *args, **options):
        admin_email = config('ADMIN_EMAIL', default=None)
        admin_password = config('ADMIN_PASSWORD', default=None)
        admin_full_name = config('ADMIN_FULL_NAME', default='Admin')

        if not admin_email or not admin_password:
            self.stdout.write(
                self.style.WARNING('ADMIN_EMAIL and ADMIN_PASSWORD environment variables are not set. Skipping admin creation.')
            )
            return

        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Admin user with email {admin_email} already exists. Skipping creation.')
            )
            return

        try:
            User.objects.create_superuser(
                email=admin_email,
                full_name=admin_full_name,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {admin_email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )
