from django.contrib.auth import get_user_model

from apps.courses.models import Course, CourseTemplate
from apps.surveys.models import QuestionBank, Survey, SurveyTemplate
from apps.tasks.models import Task, TaskTemplate


def ensure_question_bank():
    if QuestionBank.objects.exists():
        return QuestionBank.objects.count()

    questions = [
        {
            'question_text': 'How often do you use our product?',
            'question_type': 'multiple_choice',
            'category': 'market_research',
            'options': ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never'],
        },
        {
            'question_text': 'What is your age range?',
            'question_type': 'dropdown',
            'category': 'market_research',
            'options': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
        },
        {
            'question_text': 'How satisfied are you with our product?',
            'question_type': 'rating',
            'category': 'product_feedback',
            'min_value': 1,
            'max_value': 5,
        },
        {
            'question_text': 'How likely are you to recommend us to a friend?',
            'question_type': 'rating',
            'category': 'customer_satisfaction',
            'min_value': 1,
            'max_value': 10,
        },
        {
            'question_text': 'What is your opinion on current economic trends?',
            'question_type': 'multiple_choice',
            'category': 'opinion',
            'options': ['Very optimistic', 'Somewhat optimistic', 'Neutral', 'Somewhat pessimistic', 'Very pessimistic'],
        },
        {
            'question_text': 'How do you spend your free time?',
            'question_type': 'checkbox',
            'category': 'lifestyle',
            'options': ['Reading', 'Sports', 'Gaming', 'Socializing', 'Traveling', 'Cooking'],
        },
        {
            'question_text': 'What is your highest level of education?',
            'question_type': 'dropdown',
            'category': 'academic',
            'options': ['High School', 'Some College', "Bachelor's Degree", "Master's Degree", 'Doctorate'],
        },
        {
            'question_text': 'What programming languages do you know?',
            'question_type': 'checkbox',
            'category': 'academic',
            'options': ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'Rust', 'Other'],
        },
    ]

    for item in questions:
        QuestionBank.objects.create(**item)
    return QuestionBank.objects.count()


def ensure_course_templates():
    templates = [
        {
            'name': 'Python Programming Fundamentals',
            'category': 'programming',
            'difficulty': 'beginner',
            'description': 'Learn the basics of Python programming from scratch.',
            'base_price': 0.00,
            'duration_hours': 20,
            'number_of_lessons': 10,
            'min_level_required': 1,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 20,
        },
        {
            'name': 'JavaScript for Beginners',
            'category': 'programming',
            'difficulty': 'beginner',
            'description': 'Master JavaScript fundamentals and frontend basics.',
            'base_price': 0.00,
            'duration_hours': 25,
            'number_of_lessons': 12,
            'min_level_required': 1,
            'required_skills': [],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 20,
        },
        {
            'name': 'Web Development with React',
            'category': 'web_development',
            'difficulty': 'intermediate',
            'description': 'Build modern web interfaces with React and related tooling.',
            'base_price': 500.00,
            'duration_hours': 30,
            'number_of_lessons': 12,
            'min_level_required': 2,
            'required_skills': ['programming'],
            'auto_generate': True,
            'generate_frequency_hours': 168,
            'max_active_courses': 20,
        },
    ]

    created = 0
    for template in templates:
        _, was_created = CourseTemplate.objects.get_or_create(name=template['name'], defaults=template)
        if was_created:
            created += 1
    return CourseTemplate.objects.filter(auto_generate=True).count(), created


def ensure_survey_templates():
    templates = [
        {
            'name': 'Daily Market Research',
            'category': 'market_research',
            'description': 'Help us understand market trends and consumer behavior.',
            'base_reward_amount': 50.00,
            'estimated_time_minutes': 10,
            'max_participants': 100,
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_surveys': 50,
        },
        {
            'name': 'Product Feedback Survey',
            'category': 'product_feedback',
            'description': 'Share your thoughts on our products and help us improve.',
            'base_reward_amount': 75.00,
            'estimated_time_minutes': 15,
            'max_participants': 50,
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_surveys': 50,
        },
        {
            'name': 'Customer Satisfaction Check',
            'category': 'customer_satisfaction',
            'description': 'Tell us about your recent experience with our services.',
            'base_reward_amount': 40.00,
            'estimated_time_minutes': 5,
            'max_participants': 200,
            'auto_generate': True,
            'generate_frequency_hours': 12,
            'max_active_surveys': 50,
        },
    ]

    created = 0
    for template in templates:
        _, was_created = SurveyTemplate.objects.get_or_create(name=template['name'], defaults=template)
        if was_created:
            created += 1
    return SurveyTemplate.objects.filter(auto_generate=True).count(), created


def ensure_task_templates():
    templates = [
        {
            'name': 'Data Entry Task',
            'task_type': 'data_entry',
            'description': 'Enter data from provided documents into our system.',
            'priority': 'medium',
            'base_budget': 150.00,
            'estimated_time_hours': 2.0,
            'deadline_hours': 48,
            'min_level_required': 1,
            'required_specializations': [],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30,
        },
        {
            'name': 'Transcription Job',
            'task_type': 'transcription',
            'description': 'Transcribe audio recordings into text format.',
            'priority': 'medium',
            'base_budget': 200.00,
            'estimated_time_hours': 3.0,
            'deadline_hours': 72,
            'min_level_required': 2,
            'required_specializations': ['writing'],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30,
        },
        {
            'name': 'Research Task',
            'task_type': 'research',
            'description': 'Conduct online research and compile clear reports.',
            'priority': 'medium',
            'base_budget': 250.00,
            'estimated_time_hours': 4.0,
            'deadline_hours': 72,
            'min_level_required': 2,
            'required_specializations': [],
            'auto_generate': True,
            'generate_frequency_hours': 24,
            'max_active_tasks': 30,
        },
    ]

    created = 0
    for template in templates:
        _, was_created = TaskTemplate.objects.get_or_create(name=template['name'], defaults=template)
        if was_created:
            created += 1
    return TaskTemplate.objects.filter(auto_generate=True).count(), created


def ensure_demo_content():
    return {
        'question_bank': ensure_question_bank(),
        'courses': ensure_course_templates()[0],
        'surveys': ensure_survey_templates()[0],
        'tasks': ensure_task_templates()[0],
    }


def ensure_generated_content():
    """Create initial live records when a deployment database is empty."""
    if not get_user_model().objects.filter(is_staff=True).exists():
        return {'courses': 0, 'surveys': 0, 'tasks': 0}

    generated = {'courses': 0, 'surveys': 0, 'tasks': 0}

    for template in CourseTemplate.objects.filter(auto_generate=True):
        title_prefix = f'{template.name} -'
        if not Course.objects.filter(title__startswith=title_prefix).exists():
            if template.generate_course():
                generated['courses'] += 1

    for template in SurveyTemplate.objects.filter(auto_generate=True):
        title_prefix = f'{template.name} -'
        if not Survey.objects.filter(title__startswith=title_prefix).exists():
            if template.generate_survey():
                generated['surveys'] += 1

    for template in TaskTemplate.objects.filter(auto_generate=True):
        title_prefix = f'{template.name} -'
        if not Task.objects.filter(title__startswith=title_prefix).exists():
            if template.generate_task():
                generated['tasks'] += 1

    return generated
