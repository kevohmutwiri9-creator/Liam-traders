from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.courses'
    verbose_name = 'Courses'

    def ready(self):
        from apps.seed_content import ensure_demo_content
        ensure_demo_content()
