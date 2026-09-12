from django.contrib import admin
from .models import Survey, Question, SurveyResponse, SurveyPartner


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    ordering = ['order']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'reward_amount', 'current_participants', 'max_participants', 'start_date', 'end_date']
    list_filter = ['status', 'category', 'min_level_required']
    search_fields = ['title', 'description', 'partner_name']
    inlines = [QuestionInline]
    readonly_fields = ['current_participants', 'created_at', 'updated_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['survey', 'question_text', 'question_type', 'order', 'is_required']
    list_filter = ['question_type', 'is_required']
    search_fields = ['question_text']


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'user', 'status', 'reward_amount', 'is_paid', 'submitted_at']
    list_filter = ['status', 'is_paid', 'submitted_at']
    search_fields = ['user__email', 'survey__title']
    readonly_fields = ['submitted_at', 'reviewed_at']

    def save_model(self, request, obj, form, change):
        previous = SurveyResponse.objects.get(pk=obj.pk) if change else None
        super().save_model(request, obj, form, change)

        from apps.wallet.reward_services import approve_reward, mark_reward_paid
        if obj.status == 'approved' and (not previous or previous.status != 'approved'):
            approve_reward(
                user=obj.user,
                amount=obj.reward_amount,
                source='survey',
                description=f'Survey reward for {obj.survey.title}',
                survey_response=obj,
            )
        if obj.is_paid and (not previous or not previous.is_paid):
            mark_reward_paid(
                user=obj.user,
                amount=obj.reward_amount,
                source='survey',
                survey_response=obj,
            )


@admin.register(SurveyPartner)
class SurveyPartnerAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'email', 'commission_rate', 'total_surveys', 'total_paid', 'is_active']
    list_filter = ['is_active']
    search_fields = ['company', 'name', 'email']
