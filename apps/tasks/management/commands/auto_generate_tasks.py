from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.tasks.models import TaskTemplate


class Command(BaseCommand):
    help = 'Auto-generate tasks from templates'

    def handle(self, *args, **options):
        self.stdout.write('Starting auto-generation of tasks...')
        
        templates = TaskTemplate.objects.filter(auto_generate=True)
        
        for template in templates:
            task = template.generate_task()
            if task:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Generated task: {task.title} from template {template.name}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipped template {template.name} - max active tasks reached'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('Task auto-generation complete!'))
