# Liam Traders - Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- Redis (for Celery)

## Backend Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- Database credentials
- M-Pesa API credentials
- Secret key

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Celery Setup (Optional)

### 1. Start Redis

```bash
redis-server
```

### 2. Start Celery Worker

```bash
celery -A config worker -l info
```

### 3. Start Celery Beat (for scheduled tasks)

```bash
celery -A config beat -l info
```

## API Documentation

Once the backend is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## Admin Dashboard

Access the Django admin at `http://localhost:8000/admin/`

## Production Deployment

### Backend

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL for production
4. Set up a production web server (Gunicorn + Nginx)
5. Configure SSL/HTTPS
6. Set up Celery with production broker

### Frontend

1. Build the application: `npm run build`
2. Start production server: `npm start`
3. Configure environment variables
4. Set up reverse proxy with Nginx

## M-Pesa Integration

To enable M-Pesa payments:
1. Get credentials from Safaricom Developer Portal
2. Add them to `.env`:
   - `MPESA_CONSUMER_KEY`
   - `MPESA_CONSUMER_SECRET`
   - `MPESA_PASSKEY`
   - `MPESA_SHORTCODE`
3. Set `MPESA_ENVIRONMENT` to `production` for live transactions

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check credentials in `.env`
- Verify database exists

### Frontend Build Errors
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Clear Next.js cache: `rm -rf .next`

### Celery Not Working
- Ensure Redis is running
- Check Celery broker URL in `.env`
- Verify Celery configuration in `config/celery.py`

## Support

For issues or questions, refer to the README.md or contact the development team.
