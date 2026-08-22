from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


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
        }
    })


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/users/', include('apps.users.urls')),
    path('api/tasks/', include('apps.tasks.urls')),
    path('api/surveys/', include('apps.surveys.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/wallet/', include('apps.wallet.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
