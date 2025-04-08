from django.db import models
from django.contrib.auth.models import User
import requests
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=50)
    account_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=16)  # Store full number
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    card_type = models.CharField(max_length=20, choices=[
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('other', 'Other')
    ], default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def masked_account_number(self):
        if len(self.account_number) >= 4:
            return self.account_number[:4] + '*' * (len(self.account_number) - 4)
        return self.account_number

    def __str__(self):
        return f"{self.account_name} - {self.masked_account_number}"

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    last_charge = models.DateField(null=True, blank=True)
    logo_url = models.URLField(max_length=500)
    website_url = models.URLField(max_length=500)
    
    def save(self, *args, **kwargs):
        if not self.logo_url:
            # Search for logo using Serper API
            headers = {
                "X-API-KEY": "45126ead9f1356ae2b5dac62f0adbf09f009728e",
                "Content-Type": "application/json"
            }
            payload = {
                "q": f"{self.item_name} logo",
                "num": 1
            }
            response = requests.post(
                "https://google.serper.dev/images",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                images = response.json().get('images', [])
                if images:
                    self.logo_url = images[0].get('imageUrl', '')
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.item_name} - Due: {self.due_date}" 

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('revenue', 'Revenue')
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_payment', 'Mobile Payment')
    ]
    
    CATEGORIES = [
        ('Housing', 'Housing'),
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Others', 'Others')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    item_name = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='Others')
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.item_name} - {self.amount} ({self.transaction_type})" 

class Goal(models.Model):
    GOAL_CATEGORIES = [
        ('savings', 'Savings'),
        ('housing', 'Housing'),
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=GOAL_CATEGORIES)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    achieved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def progress_percentage(self):
        if self.target_amount == 0:
            return 0.00
        return round((float(self.achieved_amount) / float(self.target_amount)) * 100, 2)

    def monthly_progress_percentage(self):
        if self.monthly_target == 0:
            return 0.00
        # Calculate this month's achieved amount
        current_month = timezone.now().month
        current_year = timezone.now().year
        monthly_achieved = Transaction.objects.filter(
            user=self.user,
            date__month=current_month,
            date__year=current_year,
            transaction_type='expense' if self.category != 'savings' else 'revenue'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return round((float(monthly_achieved) / float(self.monthly_target)) * 100, 2)

    def __str__(self):
        return f"{self.title} - {self.category} (${self.target_amount})"

    class Meta:
        ordering = ['end_date'] 