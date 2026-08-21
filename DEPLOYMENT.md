# Render Deployment Guide for Liam Traders

## Prerequisites

1. Push your code to a GitHub repository
2. Create a Render account at https://render.com
3. Connect your GitHub account to Render

## Deployment Steps

### 1. Deploy Backend (Django)

1. Go to Render Dashboard and click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: liam-traders-backend
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
   - **Python Version**: 3.12

5. Add Environment Variables:
   - `SECRET_KEY`: Generate a secure random key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render backend URL (e.g., `liam-traders-backend.onrender.com`)
   - `DATABASE_URL`: Will be automatically set by Render if you create a PostgreSQL database
   - `REDIS_URL`: Will be automatically set by Render if you create a Redis instance
   - `BASE_URL`: Your backend URL
   - `MPESA_CONSUMER_KEY`: Your M-Pesa consumer key
   - `MPESA_CONSUMER_SECRET`: Your M-Pesa consumer secret
   - `MPESA_PASSKEY`: Your M-Pesa passkey
   - `MPESA_SHORTCODE`: Your M-Pesa shortcode
   - `MPESA_ENVIRONMENT`: `production`
   - `MINIMUM_WITHDRAWAL`: `100`
   - `WITHDRAWAL_FEE_PERCENTAGE`: `0.02`
   - `PLATFORM_FEE_PERCENTAGE`: `0.10`

6. Create a PostgreSQL database:
   - Go to "New +" → "PostgreSQL"
   - Name it `liam-traders-db`
   - Select the same region as your web service

7. Create a Redis instance (for Celery):
   - Go to "New +" → "Redis"
   - Name it `liam-traders-redis`
   - Select the same region as your web service

6. Click "Deploy Web Service"

### 2. Deploy Frontend (Next.js)

1. Go to Render Dashboard and click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: liam-traders-frontend
   - **Environment**: Node
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `cd frontend && npm start`
   - **Node Version**: 18

5. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL (e.g., `https://liam-traders-backend.onrender.com/api`)

6. Click "Deploy Web Service"

### 3. Post-Deployment Setup

1. **Run Migrations**:
   - Go to your backend service in Render
   - Click "Shell" (if available) or use the render CLI
   - Run: `python manage.py migrate`

2. **Create Superuser**:
   - In the same shell, run:
   ```python
   python manage.py shell
   ```
   - Then:
   ```python
   from apps.users.models import User
   User.objects.create_superuser(email='admin@yourdomain.com', full_name='Admin', password='your_secure_password')
   ```

3. **Configure CORS**:
   - Update `ALLOWED_HOSTS` in your backend settings to include your frontend URL
   - Update CORS settings in `config/settings.py` to allow your frontend domain

4. **Test the Application**:
   - Access your backend at `https://liam-traders-backend.onrender.com`
   - Access your frontend at `https://liam-traders-frontend.onrender.com`
   - Test the API endpoints
   - Test the authentication flow

## Using render.yaml (Alternative Method)

Instead of manually creating services, you can use the `render.yaml` file:

1. Make sure `render.yaml` is in your repository root
2. Go to Render Dashboard
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically create all services based on the YAML file

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
