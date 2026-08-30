from django.db import migrations


def create_sample_templates(apps, schema_editor):
    SurveyTemplate = apps.get_model('surveys', 'SurveyTemplate')
    
    templates = [
        {
            'name': 'Daily Market Research',
            'category': 'market_research',
            'description': 'Help us understand market trends and consumer behavior',
            'base_reward_amount': 50.00,
            'estimated_time_minutes': 10,
            'max_participants': 100,
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_surveys': 50
        },
        {
            'name': 'Product Feedback Survey',
            'category': 'product_feedback',
            'description': 'Share your thoughts on our products and help us improve',
            'base_reward_amount': 75.00,
            'estimated_time_minutes': 15,
            'max_participants': 50,
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_surveys': 50
        },
        {
            'name': 'Customer Satisfaction Check',
            'category': 'customer_satisfaction',
            'description': 'Tell us about your recent experience with our services',
            'base_reward_amount': 40.00,
            'estimated_time_minutes': 5,
            'max_participants': 200,
            'auto_generate': True,
            'generate_frequency_hours': 12,
            'max_active_surveys': 50
        },
        {
            'name': 'Opinion Poll',
            'category': 'opinion',
            'description': 'Share your opinion on current events and social issues',
            'base_reward_amount': 30.00,
            'estimated_time_minutes': 8,
            'max_participants': 500,
            'auto_generate': True,
            'generate_frequency_hours': 6,
            'max_active_surveys': 100
        },
        {
            'name': 'Lifestyle Survey',
            'category': 'lifestyle',
            'description': 'Help us understand lifestyle trends and preferences',
            'base_reward_amount': 45.00,
            'estimated_time_minutes': 12,
            'max_participants': 150,
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_surveys': 50
        },
        {
            'name': 'Trading Experience Survey',
            'category': 'opinion',
            'description': 'Share your trading experience and preferences',
            'base_reward_amount': 60.00,
            'estimated_time_minutes': 15,
            'max_participants': 200,
            'auto_generate': True,
            'generate_frequency_hours': 12,
            'max_active_surveys': 50
        },
        {
            'name': 'Financial Literacy Assessment',
            'category': 'academic',
            'description': 'Test your financial knowledge and trading concepts',
            'base_reward_amount': 80.00,
            'estimated_time_minutes': 20,
            'max_participants': 100,
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_surveys': 50
        },
    ]
    
    for t in templates:
        SurveyTemplate.objects.create(**t)


class Migration(migrations.Migration):
    dependencies = [
        ('surveys', '0003_populate_question_bank'),
    ]

    operations = [
        migrations.RunPython(create_sample_templates),
    ]
