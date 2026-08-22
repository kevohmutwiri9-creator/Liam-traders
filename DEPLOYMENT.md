# Render Deployment Guide for Liam Traders

## Prerequisites

1. Push your code to a GitHub repository
2. Create a Render account at https://render.com
3. Connect your GitHub account to Render

## Deployment Steps (Manual Setup)

### 1. Create PostgreSQL Database

1. Go to Render Dashboard and click "New +"
2. Select "PostgreSQL"
3. Configure:
   - **Name**: liam-traders-db
   - **Database**: liam_traders
   - **User**: liam_traders
   - **Region**: Choose a region (e.g., Oregon)
4. Click "Create Database"

### 2. Create Redis Instance

1. Go to Render Dashboard and click "New +"
2. Select "Redis"
3. Configure:
   - **Name**: liam-traders-redis
   - **Region**: Same as your database
   - **Maxmemory Policy**: allkeys-lru
4. Click "Create Redis"

### 3. Deploy Backend (Django)

1. Go to Render Dashboard and click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: liam-traders-backend
   - **Region**: Same as your database
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py create_admin && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 4`

5. Add Environment Variables:
   - `PYTHON_VERSION`: `3.12`
   - `SECRET_KEY`: Generate a secure random key (use: https://djecrety.ir/)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render backend URL (e.g., `liam-traders-backend.onrender.com,localhost,127.0.0.1`)
   - `DATABASE_URL`: Will be automatically set by Render when you connect the database
   - `REDIS_URL`: Will be automatically set by Render when you connect Redis
   - `BASE_URL`: Your backend URL
   - `ADMIN_EMAIL`: Your admin email (e.g., `kevohmutwiri9@gmail.com`)
   - `ADMIN_PASSWORD`: Your admin password (e.g., `kevoh2071M@`)
   - `ADMIN_FULL_NAME`: Your admin full name (e.g., `Admin`)
   - `MPESA_CONSUMER_KEY`: Your M-Pesa consumer key
   - `MPESA_CONSUMER_SECRET`: Your M-Pesa consumer secret
   - `MPESA_PASSKEY`: Your M-Pesa passkey
   - `MPESA_SHORTCODE`: Your M-Pesa shortcode
   - `MPESA_ENVIRONMENT`: `production`
   - `MINIMUM_WITHDRAWAL`: `100`
   - `WITHDRAWAL_FEE_PERCENTAGE`: `0.02`
   - `PLATFORM_FEE_PERCENTAGE`: `0.10`

6. Connect Database:
   - Scroll down to "Databases"
   - Select your `liam-traders-db` database
   - The `DATABASE_URL` environment variable will be automatically added

7. Connect Redis:
   - Scroll down to "Redis"
   - Select your `liam-traders-redis` instance
   - The `REDIS_URL` environment variable will be automatically added

8. Click "Deploy Web Service"

### 4. Post-Deployment Setup

The build command automatically handles:
- Database migrations
- Admin user creation (if ADMIN_EMAIL and ADMIN_PASSWORD are set)
- Static files collection

1. **Test the Application**:
   - Access your backend at `https://liam-traders-backend.onrender.com`
   - Access admin panel at `https://liam-traders-backend.onrender.com/admin`
   - Login with the admin credentials you set in environment variables
   - Test the API endpoints

## Troubleshooting

### Build Failures
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python/Node versions match

### Database Connection Issues
- Ensure DATABASE_URL is set correctly
- Check that the database is in the same region as your web service
- Verify database credentials

### Static Files
- WhiteNoise is configured for serving static files
- Run `python manage.py collectstatic` during build if needed

### M-Pesa Integration
- Ensure all M-Pesa credentials are set correctly
- Test in sandbox environment before going to production
- Verify callback URLs are accessible from M-Pesa servers

## Monitoring

- Monitor logs in Render dashboard
- Set up error tracking (e.g., Sentry)
- Monitor database usage
- Check Redis connection for Celery tasks

## Scaling

- Render automatically scales based on traffic
- Consider upgrading to paid plans for better performance
- Add a CDN for static assets if needed
- Consider separate services for Celery workers in production
