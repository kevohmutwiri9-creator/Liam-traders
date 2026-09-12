from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import Earning, Transaction, Wallet
from apps.users.models import Notification


@transaction.atomic
def approve_reward(*, user, amount, source, description, survey_response=None, task_submission=None):
    """Credit an approved reward once and keep wallet records in sync."""
    amount = Decimal(str(amount))
    wallet, _ = Wallet.objects.get_or_create(user=user)

    relation_filter = {}
    if survey_response is not None:
        relation_filter['survey_response'] = survey_response
    if task_submission is not None:
        relation_filter['task_submission'] = task_submission

    earning = Earning.objects.filter(user=user, source=source, **relation_filter).first()
    if earning is None:
        earning = Earning.objects.create(
            user=user,
            source=source,
            amount=amount,
            survey_response=survey_response,
            task_submission=task_submission,
            is_approved=True,
            approved_at=timezone.now(),
        )

    if not earning.is_approved:
        earning.is_approved = True
        earning.approved_at = timezone.now()
        earning.save(update_fields=['is_approved', 'approved_at'])

    transaction_record, _ = Transaction.objects.get_or_create(
        user=user,
        transaction_type='survey_reward' if source == 'survey' else 'task_payment',
        survey_response=survey_response,
        task_submission=task_submission,
        defaults={
            'amount': amount,
            'description': description,
            'fee_amount': Decimal('0.00'),
            'net_amount': amount,
            'status': 'pending',
        },
    )

    if not transaction_record.status == 'completed':
        wallet.add_pending(amount)
        user.pending_balance = Decimal(str(user.pending_balance)) + amount
        user.total_earnings = Decimal(str(user.total_earnings)) + amount
        user.save(update_fields=['pending_balance', 'total_earnings', 'updated_at'])

    Notification.objects.get_or_create(
        user=user,
        title=f'{source.title()} reward approved',
        defaults={
            'type': 'payment',
            'message': f'{description}. KES {amount} was added to your pending wallet balance.',
            'notification_type': 'reward',
            'action_url': '/dashboard/wallet',
        },
    )
    return earning


@transaction.atomic
def mark_reward_paid(*, user, amount, source, survey_response=None, task_submission=None):
    """Move an approved reward from pending to available exactly once."""
    amount = Decimal(str(amount))
    wallet, _ = Wallet.objects.get_or_create(user=user)
    earning = Earning.objects.filter(user=user, source=source, survey_response=survey_response, task_submission=task_submission).first()
    transaction_type = 'survey_reward' if source == 'survey' else 'task_payment'
    transaction_record = Transaction.objects.filter(
        user=user,
        transaction_type=transaction_type,
        survey_response=survey_response,
        task_submission=task_submission,
    ).first()

    if transaction_record and transaction_record.status == 'completed':
        return

    if Decimal(str(wallet.pending_balance)) >= amount:
        wallet.approve_earnings(amount)
        user.pending_balance = max(Decimal('0.00'), Decimal(str(user.pending_balance)) - amount)
        user.available_balance = Decimal(str(user.available_balance)) + amount
    else:
        wallet.total_earnings += amount
        wallet.available_balance += amount
        wallet.save(update_fields=['total_earnings', 'available_balance', 'updated_at'])
        user.available_balance = Decimal(str(user.available_balance)) + amount
        user.total_earnings = Decimal(str(user.total_earnings)) + amount

    user.save(update_fields=['pending_balance', 'available_balance', 'total_earnings', 'updated_at'])

    if earning:
        earning.is_paid = True
        earning.paid_at = timezone.now()
        earning.save(update_fields=['is_paid', 'paid_at'])
    if transaction_record:
        transaction_record.status = 'completed'
        transaction_record.completed_at = timezone.now()
        transaction_record.save(update_fields=['status', 'completed_at', 'updated_at'])
