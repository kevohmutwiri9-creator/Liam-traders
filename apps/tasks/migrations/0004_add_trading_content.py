from django.db import migrations


def add_trading_content(apps, schema_editor):
    TaskTemplate = apps.get_model('tasks', 'TaskTemplate')
    
    templates = [
        {
            'name': 'Market Analysis Task',
            'task_type': 'research',
            'description': 'Analyze market trends and trading patterns. Research financial data and provide insights on market movements.',
            'priority': 'high',
            'base_budget': 500.00,
            'estimated_time_hours': 6.0,
            'deadline_hours': 96,
            'min_level_required': 3,
            'required_specializations': [],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 3
        },
        {
            'name': 'Trading Signal Verification',
            'task_type': 'data_analysis',
            'description': 'Verify and validate trading signals and indicators. Check accuracy of trading algorithms and provide feedback.',
            'priority': 'high',
            'base_budget': 600.00,
            'estimated_time_hours': 8.0,
            'deadline_hours': 120,
            'min_level_required': 3,
            'required_specializations': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 48,
            'max_active_tasks': 2
        },
        {
            'name': 'Financial Content Creation',
            'task_type': 'content_creation',
            'description': 'Create educational content about trading, investing, and financial markets. Write articles, guides, or tutorials.',
            'priority': 'medium',
            'base_budget': 400.00,
            'estimated_time_hours': 5.0,
            'deadline_hours': 96,
            'min_level_required': 2,
            'required_specializations': ['writing'],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 4
        },
    ]
    
    for t in templates:
        TaskTemplate.objects.create(**t)


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0003_create_sample_templates'),
    ]

    operations = [
        migrations.RunPython(add_trading_content),
    ]
