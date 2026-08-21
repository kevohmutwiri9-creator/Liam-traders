from rest_framework import serializers
from .models import Survey, Question, SurveyResponse, SurveyPartner


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Survey
        fields = '__all__'
        read_only_fields = ['current_participants', 'created_at', 'updated_at']


class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    
    class Meta:
        model = Survey
        fields = '__all__'
        read_only_fields = ['current_participants', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        survey = Survey.objects.create(**validated_data)
        
        for question_data in questions_data:
            Question.objects.create(survey=survey, **question_data)
        
        survey.number_of_questions = len(questions_data)
        survey.save()
        
        return survey


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'
        read_only_fields = ['user', 'status', 'quality_score', 'reviewed_by', 
                          'review_notes', 'is_paid', 'submitted_at', 'reviewed_at']


class SurveySubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['answers', 'completion_time_seconds']
    
    def validate(self, attrs):
        survey = self.context['survey']
        user = self.context['request'].user
        
        # Check if user already responded
        if SurveyResponse.objects.filter(survey=survey, user=user).exists():
            raise serializers.ValidationError("You have already completed this survey")
        
        # Check if survey is active
        if not survey.is_active:
            raise serializers.ValidationError("This survey is not currently active")
        
        # Check if user meets level requirement
        if user.level < survey.min_level_required:
            raise serializers.ValidationError(
                f"You need to be at least Level {survey.min_level_required} to complete this survey"
            )
        
        # Check if survey has reached max participants
        if survey.current_participants >= survey.max_participants:
            raise serializers.ValidationError("This survey has reached maximum participants")
        
        return attrs


class SurveyResponseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['status', 'quality_score', 'review_notes']


class SurveyPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyPartner
        fields = '__all__'
