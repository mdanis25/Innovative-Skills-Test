from django.db import models
from purchase.models import Purchase
from django.utils import timezone

class Installment(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='installments')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
  
    def __str__(self):
        return f'Installment for Purchase  {self.purchase.purchase_id} - Amount: {self.paid_amount} - Due Date: {self.due_date}' 
 