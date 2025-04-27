from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at']
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    list_filter = ('created_at', 'updated_at')
