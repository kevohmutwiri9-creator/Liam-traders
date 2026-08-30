from django.db import migrations


def increase_template_limits(apps, schema_editor):
    TaskTemplate = apps.get_model('tasks', 'TaskTemplate')
    
    # Increase max_active_tasks for all templates
    for template in TaskTemplate.objects.all():
        if template.name == 'Microtask Batch':
            template.max_active_tasks = 50
        else:
            template.max_active_tasks = 30
        template.save()


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0004_add_trading_content'),
    ]

    operations = [
        migrations.RunPython(increase_template_limits),
    ]
