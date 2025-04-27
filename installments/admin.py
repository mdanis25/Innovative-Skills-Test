from django.contrib import admin
from installments.models import Installment 

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'paid_amount', 'payment_date', 'due_date', 'status', 'created_at', 'updated_at']
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('purchase__user__username',)
    ordering = ('-created_at',)