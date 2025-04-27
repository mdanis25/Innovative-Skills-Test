from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Installment
from django.db.models import Sum
from celery import shared_task
from django.core.mail import send_mail
from .models import Installment
from django.utils import timezone

@shared_task
def send_due_installment_reminders(purchase_id):
    from purchase.models import Purchase  # avoid circular import

    try:
        purchase = Purchase.objects.get(id=purchase_id)
        user = purchase.customer  # Or however you relate purchase to user

        # Find pending installments for this purchase
        pending_installments = purchase.installments.filter(status='pending', due_date__gt=timezone.now())

        for installment in pending_installments:
            send_mail(
                subject='Upcoming Installment Due Reminder',
                message=f'Dear {user.username},\n\nYou have an installment of {installment.paid_amount} due on {installment.due_date.date()} for Purchase ID {purchase.purchase_id}.\n\nPlease make the payment before the due date.',
                from_email='noreply@yourapp.com',
                recipient_list=[user.email],
            )
    except Purchase.DoesNotExist:
        pass
