from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.surveys.models import SurveyTemplate, QuestionBank


class Command(BaseCommand):
    help = 'Auto-generate surveys from templates'

    def handle(self, *args, **options):
        self.stdout.write('Starting auto-generation of surveys...')
        
        templates = SurveyTemplate.objects.filter(auto_generate=True)
        
        for template in templates:
            survey = template.generate_survey()
            if survey:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Generated survey: {survey.title} from template {template.name}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skipped template {template.name} - max active surveys reached'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('Survey auto-generation complete!'))
