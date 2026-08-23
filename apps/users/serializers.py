from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Skill, Education, WorkExperience, Notification

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    full_name = serializers.CharField(required=True, max_length=255)
    referral_code = serializers.CharField(required=False, max_length=20, allow_blank=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 're_password', 'referral_code']
    
    def validate_referral_code(self, value):
        """Validate referral code if provided"""
        if value:
            try:
                referrer = User.objects.get(referral_code=value)
                return referrer
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code")
        return None
    
    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        referrer = None
        
        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
                validated_data['referred_by'] = referrer
            except User.DoesNotExist:
                pass  # Invalid referral code, just ignore
        
        user = User.objects.create_user(**validated_data)
        
        # Generate referral code for new user
        user.generate_referral_code()
        
        # Award referral bonus to referrer
        if referrer:
            from django.conf import settings
            referral_bonus = getattr(settings, 'REFERRAL_BONUS', 50.00)
            referrer.add_referral_earning(referral_bonus)
            referrer.total_referrals += 1
            referrer.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone_number', 'profile_picture',
            'bio', 'location', 'level', 'total_tasks_completed', 'quality_score',
            'specialization', 'skills', 'is_identity_verified', 'total_earnings',
            'available_balance', 'pending_balance', 'reputation_score',
            'positive_reviews', 'negative_reviews', 'created_at',
            'referral_code', 'referral_earnings', 'total_referrals'
        ]
        read_only_fields = ['id', 'level', 'total_tasks_completed', 'quality_score',
                          'total_earnings', 'available_balance', 'pending_balance',
                          'reputation_score', 'positive_reviews', 'negative_reviews',
                          'referral_code', 'referral_earnings', 'total_referrals']


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
