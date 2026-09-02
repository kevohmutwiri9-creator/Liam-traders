from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Skill, Education, WorkExperience, Notification, LevelUpgradePayment

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    full_name = serializers.CharField(required=True, max_length=255)
    re_password = serializers.CharField(required=True, write_only=True)
    referral_code = serializers.CharField(required=False, max_length=20, allow_blank=True, trim_whitespace=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 're_password', 'referral_code']

    def validate_referral_code(self, value):
        """Accept a referral code string and ignore invalid inputs."""
        if not value or not value.strip():
            return ''

        code = value.strip()
        if not User.objects.filter(referral_code=code).exists():
            return ''
        return code

    def validate(self, attrs):
        re_password = attrs.pop('re_password', None)

        if re_password is not None and attrs.get('password') != re_password:
            raise serializers.ValidationError({'re_password': 'Passwords must match.'})

        attrs = super().validate(attrs)
        referral_code = attrs.get('referral_code')
        self.referrer = None

        if referral_code:
            try:
                self.referrer = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                self.referrer = None

        return attrs

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', '')
        referrer = getattr(self, 'referrer', None)

        user = User.objects.create_user(**validated_data)
        if referrer:
            user.referred_by = referrer
            user.save(update_fields=['referred_by'])

        # Generate referral code for new user
        user.generate_referral_code()

        # Award referral bonus to referrer based on tier
        if referrer:
            from django.conf import settings
            bonus_tiers = getattr(settings, 'REFERRAL_BONUS_TIERS', {1: 50.00})

            # Calculate bonus based on referrer's current tier
            current_bonus = bonus_tiers.get(1, 50.00)
            for threshold, bonus in sorted(bonus_tiers.items(), reverse=True):
                if referrer.total_referrals >= threshold:
                    current_bonus = bonus
                    break

            referrer.add_referral_earning(current_bonus)
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


class LevelUpgradePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelUpgradePayment
        fields = ['id', 'user', 'target_level', 'amount', 'transaction_reference', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']
    
    def validate_transaction_reference(self, value):
        """Ensure transaction reference is unique"""
        if LevelUpgradePayment.objects.filter(transaction_reference=value).exists():
            raise serializers.ValidationError("This transaction reference has already been used")
        return value
    
    def validate_target_level(self, value):
        """Validate target level"""
        user = self.context['request'].user
        if value <= user.level:
            raise serializers.ValidationError(f"You are already at Level {user.level} or higher")
        if value > 5:
            raise serializers.ValidationError("Maximum level is 5")
        return value


class PaymentApprovalSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    notes = serializers.CharField(required=False, allow_blank=True)
