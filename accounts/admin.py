from django.contrib import admin
from .models import BankAccount, Bill, Transaction, Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'target_amount', 'achieved_amount', 'progress_percentage', 'start_date', 'end_date')
    list_filter = ('category', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ('end_date', 'category') 