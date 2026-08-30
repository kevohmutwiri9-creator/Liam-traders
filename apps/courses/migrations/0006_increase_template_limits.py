from django.db import migrations


def increase_template_limits(apps, schema_editor):
    CourseTemplate = apps.get_model('courses', 'CourseTemplate')
    
    # Increase max_active_courses for all templates
    for template in CourseTemplate.objects.all():
        if template.max_active_courses < 20:
            template.max_active_courses = 20
            template.save()


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0005_increase_course_limits'),
    ]

    operations = [
        migrations.RunPython(increase_template_limits),
    ]
