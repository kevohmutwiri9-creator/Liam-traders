from django.db import migrations


def populate_question_bank(apps, schema_editor):
    QuestionBank = apps.get_model('surveys', 'QuestionBank')
    
    questions = [
        # Market Research
        {
            'question_text': 'How often do you use our product?',
            'question_type': 'multiple_choice',
            'category': 'market_research',
            'options': ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
        },
        {
            'question_text': 'What is your age range?',
            'question_type': 'dropdown',
            'category': 'market_research',
            'options': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        },
        {
            'question_text': 'What is your annual income range?',
            'question_type': 'dropdown',
            'category': 'market_research',
            'options': ['Under $25,000', '$25,000-$50,000', '$50,000-$75,000', '$75,000-$100,000', 'Over $100,000']
        },
        # Product Feedback
        {
            'question_text': 'How satisfied are you with our product?',
            'question_type': 'rating',
            'category': 'product_feedback',
            'min_value': 1,
            'max_value': 5
        },
        {
            'question_text': 'What features do you like most?',
            'question_type': 'checkbox',
            'category': 'product_feedback',
            'options': ['Ease of use', 'Performance', 'Design', 'Price', 'Customer support']
        },
        {
            'question_text': 'What would you improve?',
            'question_type': 'text',
            'category': 'product_feedback'
        },
        # Customer Satisfaction
        {
            'question_text': 'How likely are you to recommend us to a friend?',
            'question_type': 'rating',
            'category': 'customer_satisfaction',
            'min_value': 1,
            'max_value': 10
        },
        {
            'question_text': 'How was your recent interaction with our support team?',
            'question_type': 'multiple_choice',
            'category': 'customer_satisfaction',
            'options': ['Excellent', 'Good', 'Average', 'Poor', 'Very Poor']
        },
        # Opinion
        {
            'question_text': 'What is your opinion on current economic trends?',
            'question_type': 'multiple_choice',
            'category': 'opinion',
            'options': ['Very optimistic', 'Somewhat optimistic', 'Neutral', 'Somewhat pessimistic', 'Very pessimistic']
        },
        {
            'question_text': 'What social issues are most important to you?',
            'question_type': 'checkbox',
            'category': 'opinion',
            'options': ['Environment', 'Education', 'Healthcare', 'Economy', 'Social Justice']
        },
        # Lifestyle
        {
            'question_text': 'How do you spend your free time?',
            'question_type': 'checkbox',
            'category': 'lifestyle',
            'options': ['Reading', 'Sports', 'Gaming', 'Socializing', 'Traveling', 'Cooking']
        },
        {
            'question_text': 'What type of content do you consume most?',
            'question_type': 'multiple_choice',
            'category': 'lifestyle',
            'options': ['News', 'Entertainment', 'Educational', 'Sports', 'Technology']
        },
        # Academic
        {
            'question_text': 'What is your highest level of education?',
            'question_type': 'dropdown',
            'category': 'academic',
            'options': ['High School', 'Some College', 'Bachelor\'s Degree', 'Master\'s Degree', 'Doctorate']
        },
        {
            'question_text': 'What field of study are you interested in?',
            'question_type': 'multiple_choice',
            'category': 'academic',
            'options': ['STEM', 'Business', 'Arts', 'Humanities', 'Social Sciences']
        },
    ]
    
    for q in questions:
        QuestionBank.objects.create(**q)


class Migration(migrations.Migration):
    dependencies = [
        ('surveys', '0002_questionbank_surveytemplate'),
    ]

    operations = [
        migrations.RunPython(populate_question_bank),
    ]
