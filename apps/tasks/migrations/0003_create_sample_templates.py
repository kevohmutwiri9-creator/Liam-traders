from django.db import migrations


def create_sample_templates(apps, schema_editor):
    TaskTemplate = apps.get_model('tasks', 'TaskTemplate')
    
    templates = [
        {
            'name': 'Data Entry Task',
            'task_type': 'data_entry',
            'description': 'Enter data from provided documents into our system. Accuracy and attention to detail required.',
            'priority': 'medium',
            'base_budget': 150.00,
            'estimated_time_hours': 2.0,
            'deadline_hours': 48,
            'min_level_required': 1,
            'required_specializations': [],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30
        },
        {
            'name': 'Transcription Job',
            'task_type': 'transcription',
            'description': 'Transcribe audio recordings into text format. Good listening skills and typing accuracy required.',
            'priority': 'medium',
            'base_budget': 200.00,
            'estimated_time_hours': 3.0,
            'deadline_hours': 72,
            'min_level_required': 2,
            'required_specializations': ['writing'],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30
        },
        {
            'name': 'Data Labeling Project',
            'task_type': 'data_labeling',
            'description': 'Label and categorize data for machine learning training. Consistency and accuracy important.',
            'priority': 'high',
            'base_budget': 300.00,
            'estimated_time_hours': 4.0,
            'deadline_hours': 96,
            'min_level_required': 2,
            'required_specializations': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 48,
            'max_active_tasks': 30
        },
        {
            'name': 'AI Evaluation Task',
            'task_type': 'ai_evaluation',
            'description': 'Evaluate and provide feedback on AI-generated content. Critical thinking and analytical skills required.',
            'priority': 'high',
            'base_budget': 400.00,
            'estimated_time_hours': 5.0,
            'deadline_hours': 120,
            'min_level_required': 3,
            'required_specializations': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 48,
            'max_active_tasks': 30
        },
        {
            'name': 'Research Task',
            'task_type': 'research',
            'description': 'Conduct online research on specified topics and compile comprehensive reports. Strong research skills needed.',
            'priority': 'medium',
            'base_budget': 250.00,
            'estimated_time_hours': 4.0,
            'deadline_hours': 72,
            'min_level_required': 2,
            'required_specializations': [],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30
        },
        {
            'name': 'Content Writing',
            'task_type': 'content_creation',
            'description': 'Write engaging content for blogs, articles, or social media. Creativity and strong writing skills required.',
            'priority': 'medium',
            'base_budget': 350.00,
            'estimated_time_hours': 5.0,
            'deadline_hours': 96,
            'min_level_required': 2,
            'required_specializations': ['writing'],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30
        },
        {
            'name': 'Website Testing',
            'task_type': 'testing',
            'description': 'Test websites and applications for bugs, usability issues, and performance problems. Detail-oriented approach needed.',
            'priority': 'high',
            'base_budget': 300.00,
            'estimated_time_hours': 4.0,
            'deadline_hours': 72,
            'min_level_required': 2,
            'required_specializations': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 48,
            'max_active_tasks': 30
        },
        {
            'name': 'Microtask Batch',
            'task_type': 'microtask',
            'description': 'Complete small, quick tasks like image tagging, text classification, or simple data verification.',
            'priority': 'low',
            'base_budget': 50.00,
            'estimated_time_hours': 0.5,
            'deadline_hours': 24,
            'min_level_required': 1,
            'required_specializations': [],
            'auto_generate': True,
            'generate_frequency_hours': 12,
            'max_active_tasks': 50
        },
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
            'max_active_tasks': 30
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
            'max_active_tasks': 30
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
            'max_active_tasks': 30
        },
    ]
    
    for t in templates:
        TaskTemplate.objects.create(**t)


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0002_tasktemplate'),
    ]

    operations = [
        migrations.RunPython(create_sample_templates),
    ]
