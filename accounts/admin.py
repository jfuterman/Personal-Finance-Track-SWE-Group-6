from django.contrib import admin
from .models import BankAccount, Bill, Transaction, Goal, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'monthly_target',
        'achieved_amount',
        'monthly_progress_percentage',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
    )
    search_fields = (
        'title',
    )
    ordering = (
        '-created_at',
    )

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {'fields': ('phone_number', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {'fields': ('phone_number', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)