from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomPasswordChangeForm
from .models import BankAccount, Bill, Transaction, Goal
import random
from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import google.generativeai as genai
from django.conf import settings
from collections import defaultdict
import json
from django.db.models import Sum
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('overview')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('overview')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('overview')

@login_required
def overview(request):
    current_date = timezone.now()
    
    # Get total balance from all accounts
    total_balance = BankAccount.objects.filter(user=request.user).aggregate(
        total=Sum('balance'))['total'] or 0
    
    # Get current goals
    goals = Goal.objects.filter(user=request.user)
    savings_goal = goals.filter(category='savings').first()
    if savings_goal:
        target_achieved = savings_goal.achieved_amount
        monthly_target = savings_goal.monthly_target
        progress = savings_goal.monthly_progress_percentage()
    else:
        target_achieved = 0
        monthly_target = 0
        progress = 0
    
    # Get upcoming bills
    upcoming_bills = Bill.objects.filter(
        user=request.user,
        due_date__gte=current_date
    ).order_by('due_date')[:5]
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')[:5]
    
    # Get weekly statistics
    week_start = current_date - timedelta(days=current_date.weekday())
    week_end = week_start + timedelta(days=6)
    weekly_stats = []
    
    for i in range(7):
        day = week_start + timedelta(days=i)
        amount = Transaction.objects.filter(
            user=request.user,
            date=day
        ).aggregate(total=Sum('amount'))['total'] or 0
        weekly_stats.append({
            'day': day.strftime('%d %a'),
            'amount': float(amount)
        })
    
    # Get expenses breakdown
    expense_categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Shopping', 'Others']
    expenses_breakdown = []
    
    for category in expense_categories:
        amount = Transaction.objects.filter(
            user=request.user,
            category=category,
            transaction_type='expense',
            date__month=current_date.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get previous month's amount for comparison
        prev_month = current_date.replace(day=1) - timedelta(days=1)
        prev_amount = Transaction.objects.filter(
            user=request.user,
            category=category,
            transaction_type='expense',
            date__month=prev_month.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate percentage change
        if prev_amount > 0:
            change = ((amount - prev_amount) / prev_amount) * 100
        else:
            change = 0
            
        expenses_breakdown.append({
            'category': category,
            'amount': amount,
            'change': change,
            'change_abs': abs(change)  # Add absolute value
        })
    
    context = {
        'active_tab': 'overview',
        'current_date': current_date.strftime('%B %d, %Y'),
        'total_balance': total_balance,
        'target_achieved': target_achieved,
        'monthly_target': monthly_target,
        'progress': progress,
        'upcoming_bills': upcoming_bills,
        'recent_transactions': recent_transactions,
        'weekly_stats': weekly_stats,
        'expenses_breakdown': expenses_breakdown,
        'current_month': current_date.strftime('%B, %Y')
    }
    
    return render(request, 'overview.html', context)

@login_required
def balances(request):
    accounts = BankAccount.objects.filter(user=request.user)
    current_date = timezone.now().strftime('%B %d, %Y')
    
    # Get transactions for each account
    for account in accounts:
        account.transactions = Transaction.objects.filter(
            user=request.user,
            payment_method__icontains=account.masked_account_number[:4]  # Match transactions by first 4 digits
        ).order_by('-date')[:5]  # Get last 5 transactions
    
    return render(request, 'balances.html', {
        'active_tab': 'balances',
        'current_date': current_date,
        'accounts': accounts
    })

@login_required
def add_account(request):
    if request.method == 'POST':
        account = BankAccount(
            user=request.user,
            account_type=request.POST['account_type'],
            account_name=request.POST['account_name'],
            bank_name=request.POST['bank_name'],
            account_number=request.POST['account_number'],
            balance=request.POST['balance'],
            card_type=request.POST.get('card_type', 'other')
        )
        account.save()
    return redirect('balances')

@login_required
def remove_account(request, account_id):
    if request.method == 'POST':
        account = get_object_or_404(BankAccount, id=account_id, user=request.user)
        account.delete()
    return redirect('balances')

@login_required
def transactions(request):
    current_date = timezone.now().strftime('%B %d, %Y')
    transactions = Transaction.objects.filter(user=request.user)
    
    # Apply filters
    transaction_type = request.GET.get('transaction_type')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    if from_date:
        transactions = transactions.filter(date__gte=from_date)
    
    if to_date:
        transactions = transactions.filter(date__lte=to_date)
    
    return render(request, 'transactions.html', {
        'active_tab': 'transactions',
        'current_date': current_date,
        'transactions': transactions
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':
        transaction = Transaction(
            user=request.user,
            transaction_type=request.POST['transaction_type'],
            item_name=request.POST['item_name'],
            shop_name=request.POST['shop_name'],
            amount=request.POST['amount'],
            date=request.POST['date'],
            payment_method=request.POST['payment_method'],
            category=request.POST['category']
        )
        transaction.save()
    return redirect('transactions')

@login_required
def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
        transaction.delete()
    return redirect('transactions')

@login_required
def bills(request):
    current_date = timezone.now().strftime('%B %d, %Y')
    bills = Bill.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'bills.html', {
        'active_tab': 'bills',
        'current_date': current_date,
        'bills': bills
    })

@login_required
def add_bill(request):
    if request.method == 'POST':
        bill = Bill(
            user=request.user,
            item_name=request.POST['item_name'],
            description=request.POST['description'],
            amount=request.POST['amount'],
            due_date=request.POST['due_date'],
            website_url=request.POST['website_url']
        )
        
        if request.POST.get('last_charge'):
            bill.last_charge = request.POST['last_charge']
            
        bill.save()  # This will trigger the logo search in the save method
        
    return redirect('bills')

@login_required
def remove_bill(request, bill_id):
    if request.method == 'POST':
        bill = get_object_or_404(Bill, id=bill_id, user=request.user)
        bill.delete()
    return redirect('bills')

@login_required
def expenses(request):
    current_date = timezone.now()
    start_date = current_date - timedelta(days=365)  # Last 12 months
    
    # Get all expenses
    expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=start_date
    ).order_by('date')
    
    print(f"Found {expenses.count()} expenses")
    
    # Monthly expenses data for the graph
    monthly_data = defaultdict(float)
    yearly_data = defaultdict(float)
    
    # Ensure we have at least the last 12 months in the data
    for i in range(12):
        month_date = current_date - timedelta(days=30*i)
        month_key = month_date.strftime('%B %Y')
        monthly_data[month_key] = 0.0
    
    # Add current year and previous year to yearly data
    current_year = current_date.strftime('%Y')
    prev_year = str(int(current_year) - 1)
    yearly_data[current_year] = 0.0
    yearly_data[prev_year] = 0.0
    
    # Populate data from actual expenses
    for expense in expenses:
        month_key = expense.date.strftime('%B %Y')
        year_key = expense.date.strftime('%Y')
        amount = float(expense.amount)
        
        monthly_data[month_key] += amount
        yearly_data[year_key] += amount
    
    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys(), 
                         key=lambda x: datetime.strptime(x, '%B %Y'),
                         reverse=True)[:12]  # Get last 12 months
    sorted_months.reverse()  # Show oldest to newest
    
    # Sort years chronologically
    sorted_years = sorted(yearly_data.keys())
    
    # Prepare graph data for monthly expenses
    graph_data = {
        'labels': sorted_months,
        'values': [monthly_data[month] for month in sorted_months]
    }
    
    # Prepare graph data for yearly expenses
    yearly_graph_data = {
        'labels': sorted_years,
        'values': [yearly_data[year] for year in sorted_years]
    }
    
    print("Monthly Data:", json.dumps(graph_data, indent=2))
    print("Yearly Data:", json.dumps(yearly_graph_data, indent=2))
    
    # Categorize recent expenses
    recent_expenses = expenses.order_by('-date')[:20]  # Last 20 expenses
    categorized_expenses = defaultdict(float)
    expense_details = defaultdict(list)
    
    for expense in recent_expenses:
        category = expense.category
        amount = float(expense.amount)
        categorized_expenses[category] += amount
        
        # Store expense details for each category
        expense_details[category].append({
            'item_name': expense.item_name,
            'shop_name': expense.shop_name,
            'amount': amount,
            'date': expense.date.strftime('%Y-%m-%d')
        })
    
    # Calculate total and percentages
    total_expenses = sum(categorized_expenses.values())
    expense_breakdown = []
    categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Shopping', 'Others']
    
    for category in categories:
        amount = categorized_expenses[category]
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        expense_breakdown.append({
            'category': category,
            'amount': amount,
            'percentage': round(percentage, 1),
            'details': expense_details[category]
        })
    
    context = {
        'active_tab': 'expenses',
        'current_date': current_date.strftime('%B %d, %Y'),
        'graph_data': json.dumps(graph_data),
        'yearly_data': json.dumps(yearly_graph_data),
        'expense_breakdown': expense_breakdown,
        'total_expenses': total_expenses
    }
    
    return render(request, 'expenses.html', context)

@login_required
def goals(request):
    current_date = timezone.now()
    
    # Get or create default goals for each category
    categories = ['savings', 'housing', 'food', 'transportation', 'entertainment', 'shopping', 'others']
    for category in categories:
        # Clean up duplicate goals
        existing_goals = Goal.objects.filter(user=request.user, category=category)
        if existing_goals.count() > 1:
            # Keep the first goal and delete the rest
            first_goal = existing_goals.first()
            existing_goals.exclude(id=first_goal.id).delete()
        elif existing_goals.count() == 0:
            # Create new goal if none exists
            Goal.objects.create(
                user=request.user,
                category=category,
                title=f"{category.title()} Goal",
                target_amount=3000,
                monthly_target=250,
                start_date=current_date,
                end_date=current_date.replace(year=current_date.year + 1)
            )
    
    # Get all goals
    goals = Goal.objects.filter(user=request.user)
    savings_goal = goals.filter(category='savings').first()
    expense_goals = goals.exclude(category='savings')
    
    # Calculate daily savings data
    daily_savings = []
    current_month_days = []
    start_date = current_date.replace(day=1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    day = start_date
    while day <= end_date:
        amount = Transaction.objects.filter(
            user=request.user,
            transaction_type='revenue',
            date=day
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        daily_savings.append(float(amount))
        current_month_days.append(day.strftime('%b %d'))
        day += timedelta(days=1)
    
    # Generate available months for selection
    available_months = []
    for i in range(6):
        month_date = current_date - timedelta(days=30*i)
        available_months.append({
            'value': month_date.strftime('%Y-%m'),
            'label': month_date.strftime('%b %Y'),
            'current': i == 0
        })
    
    context = {
        'active_tab': 'goals',
        'savings_goal': savings_goal,
        'expense_goals': expense_goals,
        'daily_savings': daily_savings,
        'current_month_days': json.dumps(current_month_days),
        'current_month': current_date.strftime('%b %Y'),
        'month_range': f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}",
        'available_months': available_months
    }
    return render(request, 'goals.html', context)

@login_required
def add_goal(request):
    if request.method == 'POST':
        goal = Goal(
            user=request.user,
            title=request.POST['title'],
            category=request.POST['category'],
            target_amount=request.POST['target_amount'],
            achieved_amount=request.POST.get('achieved_amount', 0),
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            description=request.POST.get('description', '')
        )
        goal.save()
    return redirect('goals')

@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        goal.title = request.POST['title']
        goal.category = request.POST['category']
        goal.target_amount = request.POST['target_amount']
        goal.achieved_amount = request.POST['achieved_amount']
        goal.start_date = request.POST['start_date']
        goal.end_date = request.POST['end_date']
        goal.description = request.POST.get('description', '')
        goal.save()
        
    return redirect('goals')

@login_required
def delete_goal(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        goal.delete()
    return redirect('goals')

@login_required
def settings(request):
    form = CustomPasswordChangeForm(request.user)
    return render(request, 'settings.html', {'form': form})

@login_required
def update_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.username = request.POST.get('username', '')
        user.save()
        return render(request, 'settings.html', {
            'account_updated': True,
            'form': CustomPasswordChangeForm(request.user)
        })
    return redirect('settings')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            return render(request, 'settings.html', {
                'password_updated': True,
                'form': CustomPasswordChangeForm(request.user)
            })
        else:
            return render(request, 'settings.html', {
                'password_error': 'Please check your password entries and try again.',
                'form': form  # Pass back the form with errors
            })
    return redirect('settings')

@login_required
def adjust_goal(request, category):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, user=request.user, category=category)
        try:
            monthly_target = float(request.POST.get('monthly_target', goal.monthly_target))
            target_amount = float(request.POST.get('target_amount', goal.target_amount))
            
            if monthly_target < 0 or target_amount < 0:
                messages.error(request, 'Target amounts cannot be negative.')
            else:
                goal.monthly_target = monthly_target
                goal.target_amount = target_amount
                goal.save()
                messages.success(request, f'{category.title()} goal updated successfully!')
        except ValueError:
            messages.error(request, 'Please enter valid numbers for target amounts.')
    return redirect('goals')

def home(request):
    return render(request, 'home.html') 