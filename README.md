# Liam Traders - Earning & Learning Platform

A comprehensive platform for earning through legitimate work and learning skills to advance career opportunities.

## Features

### Earning System
- **Surveys**: Complete paid surveys from research partners
- **Microtasks**: Data entry, AI evaluation, transcription, research
- **Freelance Projects**: Client work across various specializations
- **Testing**: Website/app testing and feedback

### Learning System (Liam Traders Academy)
- **Programming Courses**: Python, Web Development, AI/Data
- **Skill Assessments**: Test and certify skills
- **Mentorship**: Learn from Level 5 instructors
- **Tutorials**: Step-by-step learning materials

### Level Progression System
- **Level 1 (Starter)**: Profile completion, basic tasks, platform rules
- **Level 2 (Worker)**: Microtasks, data entry, testing (50+ approved tasks)
- **Level 3 (Professional)**: Specialized freelance work, assessments
- **Level 4 (Expert)**: Programming, web development, AI projects
- **Level 5 (Academy/Master)**: Instructor, mentor, course creator

### Payment System
- **Wallet**: Pending → Approved → Withdrawable balance
- **Withdrawal Methods**: M-Pesa, Airtel Money, Bank Transfer
- **Transaction History**: Complete audit trail
- **Fraud Detection**: Security measures

## Technology Stack

### Backend
- Python/Django 4.2
- Django REST Framework
- PostgreSQL
- Redis/Celery for background jobs

### Frontend
- React/Next.js
- Tailwind CSS
- shadcn/ui components

### Infrastructure
- Cloud deployment
- HTTPS security
- Database backups
- Logging & monitoring

## Installation

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
liam_traders/
├── apps/
│   ├── users/          # User management, profiles, levels
│   ├── tasks/          # Microtasks, freelance projects
│   ├── surveys/        # Survey system
│   ├── courses/        # Academy, courses, tutorials
│   ├── wallet/         # Earnings, withdrawals, transactions
│   └── payments/       # M-Pesa, payment integrations
├── config/             # Django settings, URLs
└── frontend/           # React/Next.js frontend
```

## Revenue Streams

1. **Paid Surveys**: Commission from research providers
2. **Microtasks**: Platform fee on task completion
3. **Freelance Marketplace**: Fee on client jobs
4. **Courses**: Revenue share with instructors
5. **Corporate Work**: B2B services
6. **Advertising**: Supplementary revenue

## Security & Compliance

- User authentication (Email/Phone/OTP)
- Verified identity for higher levels
- Fraud detection systems
- Secure payment processing
- Data protection compliance

## License

Proprietary - Liam Traders
