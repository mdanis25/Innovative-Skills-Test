from django.contrib import admin
from purchase.models import Purchase 

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_id', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at', 'updated_at']
    readonly_fields = ('purchase_id', 'created_at', 'updated_at', 'total_price')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)