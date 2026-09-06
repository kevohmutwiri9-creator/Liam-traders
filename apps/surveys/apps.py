from django.apps import AppConfig


class SurveysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.surveys'
    verbose_name = 'Surveys'

    def ready(self):
        from apps.seed_content import ensure_demo_content
        ensure_demo_content()
