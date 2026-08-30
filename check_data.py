import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.surveys.models import Survey
from apps.tasks.models import Task
from apps.courses.models import Course

print(f'Active surveys count: {Survey.objects.filter(status="active").count()}')
print(f'Active tasks count: {Task.objects.filter(status="open").count()}')
print(f'Published courses count: {Course.objects.filter(status="published").count()}')

print('\nRecent surveys:')
for survey in Survey.objects.filter(status="active")[:5]:
    print(f'  - {survey.title}')

print('\nRecent tasks:')
for task in Task.objects.filter(status="open")[:5]:
    print(f'  - {task.title}')

print('\nRecent courses:')
for course in Course.objects.filter(status="published")[:5]:
    print(f'  - {course.title}')
