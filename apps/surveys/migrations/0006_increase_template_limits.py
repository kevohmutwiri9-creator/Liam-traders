from django.db import migrations


def increase_template_limits(apps, schema_editor):
    SurveyTemplate = apps.get_model('surveys', 'SurveyTemplate')
    
    # Increase max_active_surveys for all templates
    for template in SurveyTemplate.objects.all():
        if template.name == 'Opinion Poll':
            template.max_active_surveys = 100
        else:
            template.max_active_surveys = 50
        template.save()


class Migration(migrations.Migration):
    dependencies = [
        ('surveys', '0005_add_trading_programming_content'),
    ]

    operations = [
        migrations.RunPython(increase_template_limits),
    ]
