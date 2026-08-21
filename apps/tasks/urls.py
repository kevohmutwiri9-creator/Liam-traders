from django.urls import path
from .views import (
    TaskListCreateView, TaskDetailView, MyTasksView, AssignedTasksView,
    TaskApplicationListCreateView, MyApplicationsView, TaskApplicationDetailView,
    AcceptApplicationView, TaskSubmissionListCreateView, MySubmissionsView,
    TaskSubmissionDetailView, TaskReviewListCreateView, MilestoneListCreateView,
    task_statistics
)

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='tasks-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('my-tasks/', MyTasksView.as_view(), name='my-tasks'),
    path('assigned/', AssignedTasksView.as_view(), name='assigned-tasks'),
    path('<int:task_id>/applications/', TaskApplicationListCreateView.as_view(), name='task-applications'),
    path('applications/my/', MyApplicationsView.as_view(), name='my-applications'),
    path('applications/<int:pk>/', TaskApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/accept/', AcceptApplicationView.as_view(), name='accept-application'),
    path('<int:task_id>/submissions/', TaskSubmissionListCreateView.as_view(), name='task-submissions'),
    path('submissions/my/', MySubmissionsView.as_view(), name='my-submissions'),
    path('submissions/<int:pk>/', TaskSubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/<int:submission_id>/reviews/', TaskReviewListCreateView.as_view(), name='submission-reviews'),
    path('<int:task_id>/milestones/', MilestoneListCreateView.as_view(), name='task-milestones'),
    path('statistics/', task_statistics, name='task-statistics'),
]
