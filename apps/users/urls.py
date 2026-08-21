from django.urls import path
from .views import (
    UserProfileView, SkillListCreateView, SkillDetailView,
    EducationListCreateView, EducationDetailView,
    WorkExperienceListCreateView, WorkExperienceDetailView,
    NotificationListView, NotificationDetailView,
    upgrade_level, level_requirements
)

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('skills/', SkillListCreateView.as_view(), name='skills-list'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('education/', EducationListCreateView.as_view(), name='education-list'),
    path('education/<int:pk>/', EducationDetailView.as_view(), name='education-detail'),
    path('experience/', WorkExperienceListCreateView.as_view(), name='experience-list'),
    path('experience/<int:pk>/', WorkExperienceDetailView.as_view(), name='experience-detail'),
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('upgrade-level/', upgrade_level, name='upgrade-level'),
    path('level-requirements/', level_requirements, name='level-requirements'),
]
