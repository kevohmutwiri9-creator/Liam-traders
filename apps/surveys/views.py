from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Survey, Question, SurveyResponse, SurveyPartner
from .serializers import (
    SurveySerializer, SurveyCreateSerializer, SurveyResponseSerializer,
    SurveySubmitSerializer, SurveyResponseReviewSerializer, SurveyPartnerSerializer,
    QuestionSerializer
)


class SurveyListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['reward_amount', 'start_date', 'end_date']
    
    def get_queryset(self):
        queryset = Survey.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', 'active')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by user's level
        user_level = self.request.user.level
        queryset = queryset.filter(min_level_required__lte=user_level)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SurveyCreateSerializer
        return SurveySerializer


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SurveyCreateSerializer
        return SurveySerializer


class SurveyQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        return Question.objects.filter(survey_id=survey_id)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_survey_response(request, survey_id):
    try:
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SurveySubmitSerializer(
        data=request.data,
        context={'survey': survey, 'request': request}
    )
    
    if serializer.is_valid():
        # Create survey response
        response = SurveyResponse.objects.create(
            survey=survey,
            user=request.user,
            answers=serializer.validated_data['answers'],
            completion_time_seconds=serializer.validated_data['completion_time_seconds'],
            reward_amount=survey.reward_amount
        )
        
        # Update survey participant count
        survey.current_participants += 1
        survey.save()
        
        return Response({
            'message': 'Survey submitted successfully',
            'response_id': response.id,
            'reward_amount': float(response.reward_amount)
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSurveyResponsesView(generics.ListAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SurveyResponse.objects.filter(user=self.request.user)


class SurveyResponseDetailView(generics.RetrieveAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SurveyResponse.objects.filter(user=self.request.user)


class AdminSurveyResponsesView(generics.ListAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = SurveyResponse.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


class AdminSurveyResponseReviewView(generics.UpdateAPIView):
    serializer_class = SurveyResponseReviewSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SurveyResponse.objects.all()
    
    def perform_update(self, serializer):
        from django.utils import timezone
        serializer.save(
            reviewed_by=self.request.user,
            reviewed_at=timezone.now()
        )
        
        # If approved, update user's pending balance
        if serializer.validated_data.get('status') == 'approved':
            response = self.get_object()
            user = response.user
            user.pending_balance += response.reward_amount
            user.total_tasks_completed += 1
            
            # Update quality score (simplified calculation)
            current_quality = user.quality_score or 0
            new_quality = response.quality_score or 85
            user.quality_score = (current_quality + new_quality) / 2
            
            user.save()


class SurveyPartnerListCreateView(generics.ListCreateAPIView):
    serializer_class = SurveyPartnerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SurveyPartner.objects.all()


class SurveyPartnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveyPartnerSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SurveyPartner.objects.all()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def survey_statistics(request):
    user = request.user
    
    stats = {
        'total_completed': SurveyResponse.objects.filter(user=user).count(),
        'pending_review': SurveyResponse.objects.filter(user=user, status='pending').count(),
        'approved': SurveyResponse.objects.filter(user=user, status='approved').count(),
        'rejected': SurveyResponse.objects.filter(user=user, status='rejected').count(),
        'total_earned': float(
            SurveyResponse.objects.filter(
                user=user, 
                status='approved', 
                is_paid=True
            ).aggregate(total=models.Sum('reward_amount'))['total'] or 0
        ),
        'pending_earnings': float(
            SurveyResponse.objects.filter(
                user=user, 
                status='approved', 
                is_paid=False
            ).aggregate(total=models.Sum('reward_amount'))['total'] or 0
        ),
    }
    
    return Response(stats)
