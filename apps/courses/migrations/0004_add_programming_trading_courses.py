from django.db import migrations


def add_programming_trading_courses(apps, schema_editor):
    CourseTemplate = apps.get_model('courses', 'CourseTemplate')
    
    templates = [
        {
            'name': 'JavaScript for Beginners',
            'category': 'programming',
            'difficulty': 'beginner',
            'description': 'Master JavaScript fundamentals including variables, functions, DOM manipulation, and ES6+ features. Perfect for web development beginners.',
            'base_price': 0.00,
            'duration_hours': 25,
            'number_of_lessons': 12,
            'min_level_required': 1,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 3
        },
        {
            'name': 'Java Programming Mastery',
            'category': 'programming',
            'difficulty': 'intermediate',
            'description': 'Learn object-oriented programming with Java. Master classes, inheritance, polymorphism, and build robust applications.',
            'base_price': 400.00,
            'duration_hours': 30,
            'number_of_lessons': 15,
            'min_level_required': 2,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 2
        },
        {
            'name': 'C++ Programming Advanced',
            'category': 'programming',
            'difficulty': 'advanced',
            'description': 'Deep dive into C++ programming including memory management, STL, templates, and performance optimization.',
            'base_price': 600.00,
            'duration_hours': 40,
            'number_of_lessons': 20,
            'min_level_required': 3,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 336,
            'max_active_courses': 2
        },
        {
            'name': 'Full Stack Development with Node.js',
            'category': 'web_development',
            'difficulty': 'intermediate',
            'description': 'Build complete web applications with Node.js, Express, MongoDB, and React. Learn backend development and database integration.',
            'base_price': 700.00,
            'duration_hours': 45,
            'number_of_lessons': 18,
            'min_level_required': 2,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 2
        },
        {
            'name': 'Trading Fundamentals for Beginners',
            'category': 'programming',
            'difficulty': 'beginner',
            'description': 'Learn the basics of trading including market terminology, order types, risk management, and fundamental analysis.',
            'base_price': 0.00,
            'duration_hours': 15,
            'number_of_lessons': 8,
            'min_level_required': 1,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 3
        },
        {
            'name': 'Technical Analysis Mastery',
            'category': 'programming',
            'difficulty': 'intermediate',
            'description': 'Master technical analysis including chart patterns, indicators, support/resistance, and trading strategies.',
            'base_price': 500.00,
            'duration_hours': 25,
            'number_of_lessons': 12,
            'min_level_required': 2,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 2
        },
        {
            'name': 'Algorithmic Trading with Python',
            'category': 'programming',
            'difficulty': 'advanced',
            'description': 'Build automated trading systems using Python. Learn backtesting, strategy implementation, and API integration with brokers.',
            'base_price': 1200.00,
            'duration_hours': 60,
            'number_of_lessons': 25,
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
        ('courses', '0003_create_sample_templates'),
    ]

    operations = [
        migrations.RunPython(add_programming_trading_courses),
    ]
