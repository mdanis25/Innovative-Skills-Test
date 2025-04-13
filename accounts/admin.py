from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from accounts.models import CustomUser, OtpToken


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'is_active', 'is_staff', 'is_admin', 'date_join', 'last_login']
    readonly_fields = ['last_login', 'date_join']
    list_display_links = ('email',)
    list_filter = ('is_admin', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('-date_join',)
     