# Auto-Generation Setup for Production

This document explains how to set up automatic content generation for surveys, tasks, and courses on production (Render).

## Management Commands

The following Django management commands are available for auto-generation:

- `python manage.py auto_generate_surveys` - Generates surveys from templates
- `python manage.py auto_generate_tasks` - Generates tasks from templates
- `python manage.py auto_generate_courses` - Generates courses from templates

## Setting Up Cron Jobs on Render

The first task, course, and survey batches are generated during deployment. Keep the
cron jobs below enabled afterward so the catalog continues to refresh automatically.

### Option 1: Render Cron Jobs (Recommended)

Render supports cron jobs natively. Add the following to your `render.yaml` file:

```yaml
services:
  - type: cron
    name: auto-generate-surveys
    schedule: "0 */6 * * *"  # Every 6 hours
    command: python manage.py auto_generate_surveys
    
  - type: cron
    name: auto-generate-tasks
    schedule: "0 */6 * * *"  # Every 6 hours
    command: python manage.py auto_generate_tasks
    
  - type: cron
    name: auto-generate-courses
    schedule: "0 0 * * 0"  # Weekly (Sunday midnight)
    command: python manage.py auto_generate_courses
```

### Option 2: External Cron Service

If using an external cron service (like cron-job.org), set up the following jobs:

1. **Surveys Generation** (Every 6 hours):
   - URL: `https://liam-traders.onrender.com/management/auto-generate-surveys/`
   - Method: POST
   - Headers: `Authorization: Bearer YOUR_CRON_SECRET`

2. **Tasks Generation** (Every 6 hours):
   - URL: `https://liam-traders.onrender.com/management/auto-generate-tasks/`
   - Method: POST
   - Headers: `Authorization: Bearer YOUR_CRON_SECRET`

3. **Courses Generation** (Weekly):
   - URL: `https://liam-traders.onrender.com/management/auto-generate-courses/`
   - Method: POST
   - Headers: `Authorization: Bearer YOUR_CRON_SECRET`

Note: You'll need to create custom API endpoints for these if using external cron services.

## Template Configuration

Templates are configured in the database with the following settings:

- `auto_generate`: Boolean to enable/disable auto-generation
- `generate_frequency_hours`: How often to generate (in hours)
- `max_active_surveys/tasks/courses`: Maximum number of active items from this template

### Current Templates

**Surveys:**
- Daily Market Research (every 24 hours, max 5 active)
- Product Feedback Survey (every 24 hours, max 3 active)
- Customer Satisfaction Check (every 12 hours, max 10 active)
- Opinion Poll (every 6 hours, max 15 active)
- Lifestyle Survey (every 24 hours, max 5 active)

**Tasks:**
- Data Entry Task (every 24 hours, max 10 active)
- Transcription Job (every 24 hours, max 5 active)
- Data Labeling Project (every 48 hours, max 3 active)
- AI Evaluation Task (every 48 hours, max 2 active)
- Research Task (every 24 hours, max 5 active)
- Content Writing (every 24 hours, max 5 active)
- Website Testing (every 48 hours, max 3 active)
- Microtask Batch (every 12 hours, max 20 active)

**Courses:**
- Python Programming Fundamentals (weekly, max 3 active)
- Web Development with React (weekly, max 2 active)
- Data Science with Python (weekly, max 2 active)
- Mobile App Development with React Native (weekly, max 2 active)
- Machine Learning Fundamentals (bi-weekly, max 1 active)

## Manual Generation

To manually generate content, run:

```bash
python manage.py auto_generate_surveys
python manage.py auto_generate_tasks
python manage.py auto_generate_courses
```

## Monitoring

Check the logs to see what was generated:
- Successful generations show in green
- Skipped generations (max reached) show in yellow
- Errors show in red

## Customization

To add new templates or modify existing ones:

1. Access Django admin at `/admin/`
2. Navigate to the appropriate app (Surveys, Tasks, or Courses)
3. Add or modify templates
4. Set `auto_generate=True` to enable automatic generation
