from django.urls import path
from .views import dashboard, get_users, update_user, ban_user, unban_user

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', get_users, name='get-users'),
    path('users/<int:user_id>/', update_user, name='update-user'),
    path('users/<int:user_id>/ban/', ban_user, name='ban-user'),
    path('users/<int:user_id>/unban/', unban_user, name='unban-user'),
]
