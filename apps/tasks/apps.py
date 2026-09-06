from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tasks'
    verbose_name = 'Tasks'

    def ready(self):
        from apps.seed_content import ensure_demo_content
        ensure_demo_content()
