from django.core.management.base import BaseCommand

from apps.seed_content import ensure_demo_content, ensure_generated_content


class Command(BaseCommand):
    help = 'Ensure default demo courses, surveys, tasks, and question bank records exist.'

    def handle(self, *args, **options):
        data = ensure_demo_content()
        generated = ensure_generated_content()
        self.stdout.write(self.style.SUCCESS(
            f'Demo content ready: {data}; generated: {generated}'
        ))