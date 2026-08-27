from django.db import migrations


def add_trading_programming_content(apps, schema_editor):
    SurveyTemplate = apps.get_model('surveys', 'SurveyTemplate')
    QuestionBank = apps.get_model('surveys', 'QuestionBank')
    
    # Add new survey templates
    templates = [
        {
            'name': 'Trading Experience Survey',
            'category': 'opinion',
            'description': 'Share your trading experience and preferences',
            'base_reward_amount': 60.00,
            'estimated_time_minutes': 15,
            'max_participants': 200,
            'auto_generate': True,
            'generate_frequency_hours': 12,
            'max_active_surveys': 8
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
            'max_active_surveys': 5
        },
    ]
    
    for t in templates:
        SurveyTemplate.objects.create(**t)
    
    # Add trading questions
    trading_questions = [
        {
            'question_text': 'How long have you been trading?',
            'question_type': 'dropdown',
            'category': 'opinion',
            'options': ['Less than 6 months', '6-12 months', '1-2 years', '2-5 years', '5+ years']
        },
        {
            'question_text': 'What type of trading are you most interested in?',
            'question_type': 'multiple_choice',
            'category': 'opinion',
            'options': ['Stocks', 'Forex', 'Crypto', 'Commodities', 'Options']
        },
        {
            'question_text': 'What is your primary trading strategy?',
            'question_type': 'multiple_choice',
            'category': 'opinion',
            'options': ['Day trading', 'Swing trading', 'Position trading', 'Scalping', 'Long-term investing']
        },
        {
            'question_text': 'How would you rate your risk tolerance?',
            'question_type': 'rating',
            'category': 'opinion',
            'min_value': 1,
            'max_value': 10
        },
        {
            'question_text': 'What trading tools do you use regularly?',
            'question_type': 'checkbox',
            'category': 'opinion',
            'options': ['Technical indicators', 'Fundamental analysis', 'News feeds', 'Trading bots', 'Chart patterns']
        },
    ]
    
    for q in trading_questions:
        QuestionBank.objects.create(**q)
    
    # Add programming questions
    programming_questions = [
        {
            'question_text': 'What programming languages do you know?',
            'question_type': 'checkbox',
            'category': 'academic',
            'options': ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'Rust', 'Other']
        },
        {
            'question_text': 'How many years of programming experience do you have?',
            'question_type': 'dropdown',
            'category': 'academic',
            'options': ['Less than 1 year', '1-2 years', '2-5 years', '5-10 years', '10+ years']
        },
        {
            'question_text': 'What type of development do you specialize in?',
            'question_type': 'multiple_choice',
            'category': 'academic',
            'options': ['Web development', 'Mobile development', 'Data science', 'Machine learning', 'Game development', 'DevOps']
        },
        {
            'question_text': 'How confident are you in your programming skills?',
            'question_type': 'rating',
            'category': 'academic',
            'min_value': 1,
            'max_value': 10
        },
        {
            'question_text': 'What programming frameworks are you familiar with?',
            'question_type': 'checkbox',
            'category': 'academic',
            'options': ['React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'TensorFlow', 'PyTorch', 'Other']
        },
    ]
    
    for q in programming_questions:
        QuestionBank.objects.create(**q)


class Migration(migrations.Migration):
    dependencies = [
        ('surveys', '0004_create_sample_templates'),
    ]

    operations = [
        migrations.RunPython(add_trading_programming_content),
    ]
