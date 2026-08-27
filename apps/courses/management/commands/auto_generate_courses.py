from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.courses.models import CourseTemplate


class Command(BaseCommand):
    help = 'Auto-generate courses from templates'

    def handle(self, *args, **options):
        self.stdout.write('Starting auto-generation of courses...')
        
        templates = CourseTemplate.objects.filter(auto_generate=True)
        
        for template in templates:
            course = template.generate_course()
            if course:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Generated course: {course.title} from template {template.name}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipped template {template.name} - max active courses reached'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('Course auto-generation complete!'))
