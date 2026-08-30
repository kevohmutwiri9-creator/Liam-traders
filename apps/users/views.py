from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Skill, Education, WorkExperience, Notification, LevelUpgradePayment
from .serializers import (
    UserSerializer, UserUpdateSerializer, SkillSerializer,
    EducationSerializer, WorkExperienceSerializer,
    NotificationSerializer, LevelUpgradeSerializer,
    LevelUpgradePaymentSerializer, PaymentApprovalSerializer
)

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        # Ensure user has a referral code
        if not self.request.user.referral_code:
            self.request.user.generate_referral_code()
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer


class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)


class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)


class WorkExperienceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.request.user)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(is_read=True)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upgrade_level(request):
    serializer = LevelUpgradeSerializer(data={}, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Level upgraded successfully',
            'new_level': user.level
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def level_requirements(request):
    from django.conf import settings
    current_level = request.user.level
    next_level = current_level + 1
    
    requirements = {
        'current_level': current_level,
        'current_level_name': dict(User.LEVEL_CHOICES).get(current_level),
        'next_level': next_level if next_level <= 5 else None,
        'next_level_name': dict(User.LEVEL_CHOICES).get(next_level) if next_level <= 5 else None,
        'requirements': settings.LEVEL_REQUIREMENTS.get(next_level) if next_level <= 5 else None,
        'user_stats': {
            'total_tasks_completed': request.user.total_tasks_completed,
            'quality_score': float(request.user.quality_score),
            'specialization': request.user.specialization,
        },
        'can_upgrade': request.user.can_upgrade_level()
    }
    
    return Response(requirements)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def referral_leaderboard(request):
    """Get top referrers leaderboard"""
    limit = int(request.GET.get('limit', 10))
    top_referrers = User.objects.filter(
        total_referrals__gt=0
    ).order_by('-total_referrals', '-referral_earnings')[:limit]
    
    leaderboard = []
    for rank, user in enumerate(top_referrers, 1):
        leaderboard.append({
            'rank': rank,
            'user_id': user.id,
            'full_name': user.full_name,
            'email': user.email[:3] + '***@' + user.email.split('@')[1],  # Partially mask email
            'total_referrals': user.total_referrals,
            'referral_earnings': float(user.referral_earnings),
            'level': user.level,
            'level_name': dict(User.LEVEL_CHOICES).get(user.level)
        })
    
    return Response({
        'leaderboard': leaderboard,
        'total': len(leaderboard)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def referral_history(request):
    """Get referral history for current user"""
    user = request.user
    referrals = User.objects.filter(referred_by=user).order_by('-created_at')
    
    history = []
    for referral in referrals:
        history.append({
            'user_id': referral.id,
            'full_name': referral.full_name,
            'email': referral.email[:3] + '***@' + referral.email.split('@')[1],
            'created_at': referral.created_at.isoformat(),
            'level': referral.level,
            'level_name': dict(User.LEVEL_CHOICES).get(referral.level),
            'total_earnings': float(referral.total_earnings)
        })
    
    return Response({
        'referrals': history,
        'total_referrals': user.total_referrals,
        'total_earnings': float(user.referral_earnings)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def referral_stats(request):
    """Get comprehensive referral statistics for current user"""
    user = request.user
    from django.conf import settings
    
    # Calculate bonus tier
    referral_bonus = getattr(settings, 'REFERRAL_BONUS', 50.00)
    bonus_tiers = getattr(settings, 'REFERRAL_BONUS_TIERS', {
        1: 50.00,
        10: 75.00,
        25: 100.00,
        50: 150.00,
        100: 200.00
    })
    
    current_bonus = referral_bonus
    for threshold, bonus in sorted(bonus_tiers.items(), reverse=True):
        if user.total_referrals >= threshold:
            current_bonus = bonus
            break
    
    next_tier = None
    for threshold, bonus in sorted(bonus_tiers.items()):
        if user.total_referrals < threshold:
            next_tier = {
                'threshold': threshold,
                'bonus': bonus,
                'referrals_needed': threshold - user.total_referrals
            }
            break
    
    return Response({
        'total_referrals': user.total_referrals,
        'referral_earnings': float(user.referral_earnings),
        'referral_code': user.referral_code,
        'current_bonus_tier': current_bonus,
        'next_tier': next_tier,
        'bonus_tiers': bonus_tiers
    })


class LevelUpgradePaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = LevelUpgradePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LevelUpgradePayment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentApprovalView(generics.UpdateAPIView):
    serializer_class = PaymentApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only admins can approve payments
        if not self.request.user.is_staff:
            return LevelUpgradePayment.objects.none()
        return LevelUpgradePayment.objects.filter(status='pending')
    
    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            action = serializer.validated_data['action']
            notes = serializer.validated_data.get('notes', '')
            
            if action == 'approve':
                if payment.approve(request.user):
                    # Send notification to user
                    Notification.objects.create(
                        user=payment.user,
                        title='Level Upgrade Approved',
                        message=f'Your level upgrade to {dict(User.LEVEL_CHOICES).get(payment.target_level)} has been approved!',
                        notification_type='level_upgrade',
                        is_read=False
                    )
                    return Response({
                        'message': 'Payment approved and level upgraded',
                        'payment_id': payment.id
                    }, status=status.HTTP_200_OK)
                return Response(
                    {'error': 'Cannot approve this payment'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif action == 'reject':
                if payment.reject(request.user, notes):
                    # Send notification to user
                    Notification.objects.create(
                        user=payment.user,
                        title='Level Upgrade Rejected',
                        message=f'Your level upgrade request has been rejected. Reason: {notes or "Not specified"}',
                        notification_type='level_upgrade',
                        is_read=False
                    )
                    return Response({
                        'message': 'Payment rejected',
                        'payment_id': payment.id
                    }, status=status.HTTP_200_OK)
                return Response(
                    {'error': 'Cannot reject this payment'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_payments(request):
    """Get all pending payments for admin approval"""
    if not request.user.is_staff:
        return Response(
            {'error': 'Unauthorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    payments = LevelUpgradePayment.objects.filter(status='pending').select_related('user')
    data = []
    
    for payment in payments:
        data.append({
            'id': payment.id,
            'user': {
                'id': payment.user.id,
                'email': payment.user.email,
                'full_name': payment.user.full_name,
                'current_level': payment.user.level
            },
            'target_level': payment.target_level,
            'target_level_name': dict(User.LEVEL_CHOICES).get(payment.target_level),
            'amount': float(payment.amount),
            'transaction_reference': payment.transaction_reference,
            'status': payment.status,
            'created_at': payment.created_at.isoformat()
        })
    
    return Response({'payments': data, 'total': len(data)})


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def auto_generate_content(request):
    """Generate surveys, tasks, and courses from templates (admin only)"""
    from apps.surveys.models import SurveyTemplate
    from apps.tasks.models import TaskTemplate
    from apps.courses.models import CourseTemplate
    
    results = {
        'surveys': 0,
        'tasks': 0,
        'courses': 0,
        'errors': []
    }
    
    # Generate surveys
    for template in SurveyTemplate.objects.filter(auto_generate=True):
        try:
            if template.generate_survey():
                results['surveys'] += 1
        except Exception as e:
            results['errors'].append(f'Survey {template.name}: {str(e)}')
    
    # Generate tasks
    for template in TaskTemplate.objects.filter(auto_generate=True):
        try:
            if template.generate_task():
                results['tasks'] += 1
        except Exception as e:
            results['errors'].append(f'Task {template.name}: {str(e)}')
    
    # Generate courses
    for template in CourseTemplate.objects.filter(auto_generate=True):
        try:
            if template.generate_course():
                results['courses'] += 1
        except Exception as e:
            results['errors'].append(f'Course {template.name}: {str(e)}')
    
    return Response({
        'message': 'Auto-generation complete',
        'results': results
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications as read for the current user"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return Response({'message': 'All notifications marked as read'})
