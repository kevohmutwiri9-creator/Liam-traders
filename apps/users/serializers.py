from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Skill, Education, WorkExperience, Notification

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    full_name = serializers.CharField(required=True, max_length=255)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 're_password']
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'profile_picture',
            'bio', 'location', 'level', 'total_tasks_completed', 'quality_score',
            'specialization', 'skills', 'is_identity_verified', 'total_earnings',
            'available_balance', 'pending_balance', 'reputation_score',
            'positive_reviews', 'negative_reviews', 'created_at'
        ]
        read_only_fields = ['id', 'level', 'total_tasks_completed', 'quality_score',
                          'total_earnings', 'available_balance', 'pending_balance',
                          'reputation_score', 'positive_reviews', 'negative_reviews']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'profile_picture', 'bio', 'location']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['user', 'verified']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['user']


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        read_only_fields = ['user']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class LevelUpgradeSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context['request'].user
        if not user.can_upgrade_level():
            raise serializers.ValidationError(
                "You do not meet the requirements for the next level"
            )
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.upgrade_level()
        return user
