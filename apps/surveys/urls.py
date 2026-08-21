from django.urls import path
from .views import (
    SurveyListCreateView, SurveyDetailView, SurveyQuestionsView,
    submit_survey_response, UserSurveyResponsesView, SurveyResponseDetailView,
    AdminSurveyResponsesView, AdminSurveyResponseReviewView,
    SurveyPartnerListCreateView, SurveyPartnerDetailView, survey_statistics
)

urlpatterns = [
    path('', SurveyListCreateView.as_view(), name='surveys-list'),
    path('<int:pk>/', SurveyDetailView.as_view(), name='survey-detail'),
    path('<int:survey_id>/questions/', SurveyQuestionsView.as_view(), name='survey-questions'),
    path('<int:survey_id>/submit/', submit_survey_response, name='submit-survey'),
    path('my-responses/', UserSurveyResponsesView.as_view(), name='my-survey-responses'),
    path('responses/<int:pk>/', SurveyResponseDetailView.as_view(), name='survey-response-detail'),
    path('admin/responses/', AdminSurveyResponsesView.as_view(), name='admin-survey-responses'),
    path('admin/responses/<int:pk>/review/', AdminSurveyResponseReviewView.as_view(), name='admin-review-response'),
    path('admin/partners/', SurveyPartnerListCreateView.as_view(), name='survey-partners'),
    path('admin/partners/<int:pk>/', SurveyPartnerDetailView.as_view(), name='survey-partner-detail'),
    path('statistics/', survey_statistics, name='survey-statistics'),
]
