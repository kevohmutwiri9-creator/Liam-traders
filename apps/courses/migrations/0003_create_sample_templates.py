from django.db import migrations


def create_sample_templates(apps, schema_editor):
    CourseTemplate = apps.get_model('courses', 'CourseTemplate')
    
    templates = [
        {
            'name': 'Python Programming Fundamentals',
            'category': 'programming',
            'difficulty': 'beginner',
            'description': 'Learn the basics of Python programming from scratch. This course covers variables, data types, control structures, functions, and object-oriented programming.',
            'base_price': 0.00,
            'duration_hours': 20,
            'number_of_lessons': 10,
            'min_level_required': 1,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 3
        },
        {
            'name': 'Web Development with React',
            'category': 'web_development',
            'difficulty': 'intermediate',
            'description': 'Master modern web development with React. Learn components, state management, hooks, and build real-world applications.',
            'base_price': 500.00,
            'duration_hours': 30,
            'number_of_lessons': 12,
            'min_level_required': 2,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 2
        },
        {
            'name': 'Data Science with Python',
            'category': 'data_science',
            'difficulty': 'intermediate',
            'description': 'Learn data analysis, visualization, and machine learning with Python. Master pandas, numpy, matplotlib, and scikit-learn.',
            'base_price': 750.00,
            'duration_hours': 40,
            'number_of_lessons': 15,
            'min_level_required': 2,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 2
        },
        {
            'name': 'Mobile App Development with React Native',
            'category': 'mobile_development',
            'difficulty': 'intermediate',
            'description': 'Build cross-platform mobile applications using React Native. Learn navigation, state management, and native modules.',
            'base_price': 600.00,
            'duration_hours': 35,
            'number_of_lessons': 14,
            'min_level_required': 2,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 2
        },
        {
            'name': 'Machine Learning Fundamentals',
            'category': 'ai_ml',
            'difficulty': 'advanced',
            'description': 'Deep dive into machine learning algorithms and techniques. Learn supervised and unsupervised learning, neural networks, and deep learning.',
            'base_price': 1000.00,
            'duration_hours': 50,
            'number_of_lessons': 20,
            'min_level_required': 3,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 336,
            'max_active_courses': 1
        },
    ]
    
    for t in templates:
        CourseTemplate.objects.create(**t)


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0002_coursetemplate_alter_assessmentattempt_status'),
    ]

    operations = [
        migrations.RunPython(create_sample_templates),
    ]
