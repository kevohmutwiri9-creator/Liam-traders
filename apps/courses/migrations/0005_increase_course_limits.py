from django.db import migrations


def increase_course_limits(apps, schema_editor):
    CourseTemplate = apps.get_model('courses', 'CourseTemplate')
    
    # Increase max_active_courses for all templates to allow more variety
    templates = CourseTemplate.objects.all()
    for template in templates:
        if template.difficulty == 'beginner':
            template.max_active_courses = 5
        elif template.difficulty == 'intermediate':
            template.max_active_courses = 4
        elif template.difficulty == 'advanced':
            template.max_active_courses = 3
        template.save()


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0004_add_programming_trading_courses'),
    ]

    operations = [
        migrations.RunPython(increase_course_limits),
    ]
