from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Task, TaskApplication, TaskSubmission, TaskReview, Milestone
from .serializers import (
    TaskSerializer, TaskCreateSerializer, TaskApplicationSerializer,
    TaskApplicationCreateSerializer, TaskSubmissionSerializer,
    TaskSubmissionCreateSerializer, TaskSubmissionReviewSerializer,
    TaskReviewSerializer, MilestoneSerializer
)


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'task_type']
    ordering_fields = ['budget', 'deadline', 'created_at']
    
    def get_queryset(self):
        queryset = Task.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', 'open')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by task type
        task_type = self.request.query_params.get('task_type')
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        
        # Filter by user's level
        user_level = self.request.user.level
        queryset = queryset.filter(min_level_required__lte=user_level)
        
        # Filter by specialization
        if self.request.user.specialization:
            queryset = queryset.filter(
                Q(required_specializations__contains=[]) |
                Q(required_specializations__contains=[self.request.user.specialization])
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


class MyTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(client=self.request.user)


class AssignedTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TaskApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TaskApplication.objects.filter(task_id=task_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskApplicationCreateSerializer
        return TaskApplicationSerializer
    
    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = Task.objects.get(id=task_id)
        serializer.save(worker=self.request.user, task=task)
        
        # Update task application count
        task.total_applications += 1
        task.save()


class MyApplicationsView(generics.ListAPIView):
    serializer_class = TaskApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TaskApplication.objects.filter(worker=self.request.user)


class TaskApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TaskApplication.objects.all()


class AcceptApplicationView(generics.UpdateAPIView):
    serializer_class = TaskApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TaskApplication.objects.all()
    
    def perform_update(self, serializer):
        application = self.get_object()
        task = application.task
        
        # Check if user is the client
        if task.client != self.request.user:
            raise permissions.PermissionDenied("You are not the client for this task")
        
        # Update application status
        serializer.save(status='accepted')
        
        # Update task status and assignment
        task.status = 'in_progress'
        task.assigned_to = application.worker
        task.save()
        
        # Reject other applications
        TaskApplication.objects.filter(task=task).exclude(id=application.id).update(status='rejected')


class TaskSubmissionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TaskSubmission.objects.filter(task_id=task_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskSubmissionCreateSerializer
        return TaskSubmissionSerializer
    
    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = Task.objects.get(id=task_id)
        serializer.save(worker=self.request.user, task=task, amount_earned=task.budget)


class MySubmissionsView(generics.ListAPIView):
    serializer_class = TaskSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TaskSubmission.objects.filter(worker=self.request.user)


class TaskSubmissionDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TaskSubmission.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskSubmissionReviewSerializer
        return TaskSubmissionSerializer
    
    def perform_update(self, serializer):
        from django.utils import timezone
        submission = self.get_object()
        task = submission.task
        
        # Check if user is the client
        if task.client != self.request.user:
            raise permissions.PermissionDenied("You are not the client for this task")
        
        serializer.save(
            reviewed_by=self.request.user,
            reviewed_at=timezone.now()
        )
        
        # If approved, update worker's pending balance
        if serializer.validated_data.get('status') == 'approved':
            worker = submission.worker
            worker.pending_balance += submission.amount_earned
            worker.total_tasks_completed += 1
            
            # Update quality score
            current_quality = worker.quality_score or 0
            new_quality = submission.quality_score or 85
            worker.quality_score = (current_quality + new_quality) / 2
            
            worker.save()
            
            # Update task status
            task.status = 'completed'
            task.save()


class TaskReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        submission_id = self.kwargs['submission_id']
        return TaskReview.objects.filter(submission_id=submission_id)
    
    def perform_create(self, serializer):
        submission_id = self.kwargs['submission_id']
        submission = TaskSubmission.objects.get(id=submission_id)
        serializer.save(
            reviewer=self.request.user,
            worker=submission.worker,
            submission=submission
        )


class MilestoneListCreateView(generics.ListCreateAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Milestone.objects.filter(task_id=task_id)
    
    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = Task.objects.get(id=task_id)
        serializer.save(task=task)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_statistics(request):
    user = request.user
    
    stats = {
        'tasks_posted': Task.objects.filter(client=user).count(),
        'tasks_assigned': Task.objects.filter(assigned_to=user).count(),
        'applications_sent': TaskApplication.objects.filter(worker=user).count(),
        'applications_accepted': TaskApplication.objects.filter(worker=user, status='accepted').count(),
        'submissions_made': TaskSubmission.objects.filter(worker=user).count(),
        'submissions_approved': TaskSubmission.objects.filter(worker=user, status='approved').count(),
        'total_earned': float(
            TaskSubmission.objects.filter(
                worker=user,
                status='approved',
                is_paid=True
            ).aggregate(total=models.Sum('amount_earned'))['total'] or 0
        ),
        'pending_earnings': float(
            TaskSubmission.objects.filter(
                worker=user,
                status='approved',
                is_paid=False
            ).aggregate(total=models.Sum('amount_earned'))['total'] or 0
        ),
    }
    
    return Response(stats)
