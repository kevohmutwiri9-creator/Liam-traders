from rest_framework import serializers
from .models import Task, TaskApplication, TaskSubmission, TaskReview, Milestone


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['client', 'assigned_to', 'total_applications', 'views_count', 'created_at', 'updated_at']


class TaskCreateSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, required=False)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['client', 'assigned_to', 'total_applications', 'views_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        milestones_data = validated_data.pop('milestones', [])
        task = Task.objects.create(**validated_data)
        
        for milestone_data in milestones_data:
            Milestone.objects.create(task=task, **milestone_data)
        
        return task


class TaskApplicationSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source='worker.full_name', read_only=True)
    worker_level = serializers.IntegerField(source='worker.level', read_only=True)
    
    class Meta:
        model = TaskApplication
        fields = '__all__'
        read_only_fields = ['worker', 'status', 'created_at', 'updated_at']


class TaskApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskApplication
        fields = ['cover_letter', 'proposed_amount', 'estimated_completion', 'attachments']
    
    def validate(self, attrs):
        task = self.context['task']
        user = self.context['request'].user
        
        # Check if user already applied
        if TaskApplication.objects.filter(task=task, worker=user).exists():
            raise serializers.ValidationError("You have already applied to this task")
        
        # Check if task is open
        if task.status != 'open':
            raise serializers.ValidationError("This task is not currently accepting applications")
        
        # Check if user meets level requirement
        if user.level < task.min_level_required:
            raise serializers.ValidationError(
                f"You need to be at least Level {task.min_level_required} to apply for this task"
            )
        
        return attrs


class TaskSubmissionSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source='worker.full_name', read_only=True)
    
    class Meta:
        model = TaskSubmission
        fields = '__all__'
        read_only_fields = ['worker', 'status', 'amount_earned', 'is_paid', 
                          'quality_score', 'client_feedback', 'reviewed_by',
                          'submitted_at', 'reviewed_at']


class TaskSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields = ['description', 'work_files', 'hours_worked']
    
    def validate(self, attrs):
        task = self.context['task']
        user = self.context['request'].user
        
        # Check if user is assigned to this task
        if task.assigned_to != user:
            raise serializers.ValidationError("You are not assigned to this task")
        
        # Check if task is in progress
        if task.status != 'in_progress':
            raise serializers.ValidationError("Task must be in progress to submit work")
        
        return attrs


class TaskSubmissionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields = ['status', 'quality_score', 'client_feedback']


class TaskReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)
    worker_name = serializers.CharField(source='worker.full_name', read_only=True)
    
    class Meta:
        model = TaskReview
        fields = '__all__'
        read_only_fields = ['reviewer', 'worker', 'created_at']
