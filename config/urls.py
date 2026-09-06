from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.admin_dashboard.admin import liam_admin
import hashlib
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
import jwt


@api_view(['POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """
    Test endpoint to validate a token and debug authentication issues.
    POST with {'token': 'your_jwt_token'} to test if the token is valid.
    """
    token = request.data.get('token', '').replace('Bearer ', '').strip()
    
    if not token:
        return JsonResponse({
            'valid': False,
            'error': 'No token provided',
            'hint': 'Send POST request with {"token": "your_jwt_token"}',
        }, status=400)
    
    try:
        # Try to decode the token with the server's SECRET_KEY
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        
        return JsonResponse({
            'valid': True,
            'message': 'Token is valid',
            'user_id': decoded.get('user_id'),
            'exp': decoded.get('exp'),
        })
    except ExpiredSignatureError:
        return JsonResponse({
            'valid': False,
            'error': 'Token has expired',
            'error_type': 'ExpiredSignatureError',
        }, status=401)
    except InvalidSignatureError:
        secret_key_hash = hashlib.sha256(settings.SECRET_KEY.encode()).hexdigest()[:16]
        return JsonResponse({
            'valid': False,
            'error': 'Invalid token signature - SECRET_KEY mismatch',
            'error_type': 'InvalidSignatureError',
            'hint': 'Token was signed with a different SECRET_KEY than the server is using now',
            'server_secret_hash': secret_key_hash,
        }, status=401)
    except DecodeError as e:
        return JsonResponse({
            'valid': False,
            'error': f'Cannot decode token: {str(e)}',
            'error_type': 'DecodeError',
        }, status=401)
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'error': f'Validation error: {str(e)}',
            'error_type': type(e).__name__,
        }, status=400)


def api_root(request):
    return JsonResponse({
        'message': 'Liam Traders API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'auth': '/api/auth/',
            'users': '/api/users/',
            'tasks': '/api/tasks/',
            'surveys': '/api/surveys/',
            'courses': '/api/courses/',
            'wallet': '/api/wallet/',
            'payments': '/api/payments/',
            'health': '/api/health/',
            'debug': {
                'token_validate': '/api/debug/token-validate/',
            }
        }
    })


def health_check(request):
    """Health check endpoint that includes JWT configuration info for debugging."""
    secret_key = settings.SECRET_KEY
    secret_key_hash = hashlib.sha256(secret_key.encode()).hexdigest()[:16]
    
    return JsonResponse({
        'status': 'ok',
        'database': 'connected',
        'jwt_config': {
            'algorithm': settings.SIMPLE_JWT.get('ALGORITHM'),
            'access_token_lifetime_minutes': int(settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', 0).total_seconds() / 60),
            'refresh_token_lifetime_days': settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', None) and int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds() / 86400),
            'secret_key_prefix': secret_key[:10] if len(secret_key) >= 10 else '***',
            'secret_key_length': len(secret_key),
            'secret_key_hash': secret_key_hash,  # For debugging token mismatch issues
        },
        'auth_classes': settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', []),
        'debug': settings.DEBUG,
    })


urlpatterns = [
    path('', api_root),
    path('api/health/', health_check, name='health-check'),
    path('api/debug/token-validate/', validate_token, name='token-validate'),
    path('admin/', liam_admin.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/users/', include('apps.users.urls')),
    path('api/tasks/', include('apps.tasks.urls')),
    path('api/surveys/', include('apps.surveys.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/wallet/', include('apps.wallet.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/admin-dashboard/', include('apps.admin_dashboard.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
