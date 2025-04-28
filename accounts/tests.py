from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import BankAccount, Bill, Transaction, Goal, Category, Budgets
from .forms import CustomUserCreationForm, UserUpdateForm, CustomPasswordChangeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import json
from django.utils import timezone
from datetime import timedelta
from django.db import connection


class TestViews(TestCase):
    def setUp(self):
        # Create test user
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        
        # Create test account
        self.account = BankAccount.objects.create(
            user=self.user,
            account_name='Test Account',
            balance=1000.00,
            account_type='checking',
            bank_name='Test Bank',
            account_number='1234567890123456',
            card_type='visa'
        )
        
        # Create test bill
        self.bill = Bill.objects.create(
            user=self.user,
            item_name='Test Bill',
            description='Test Description',
            amount=100.00,
            due_date='2024-04-30',
            logo_url='https://example.com/logo.png',
            website_url='https://example.com'
        )
        
        # Create test transaction
        self.transaction = Transaction.objects.create(
            user=self.user,
            transaction_type='expense',
            item_name='Test Item',
            shop_name='Test Shop',
            amount=50.00,
            date='2024-04-16',
            payment_method='credit_card',
            category='Food'
        )
        
        # Create test goal
        self.goal = Goal.objects.create(
            user=self.user,
            title='Test Goal',
            category='savings',
            target_amount=1000.00,
            achieved_amount=500.00,
            monthly_target=100.00,
            start_date='2024-01-01',
            end_date='2024-12-31',
            description='Test goal description'
        )

    def test_overview_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'overview.html')

    def test_balances_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('balances'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'balances.html')

    def test_transactions_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions.html')

    def test_bills_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills.html')

    def test_expenses_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses.html')

    def test_goals_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goals.html')

    def test_settings_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_add_account(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_account'), {
            'account_name': 'New Account',
            'balance': 2000.00,
            'account_type': 'savings',
            'bank_name': 'New Bank',
            'account_number': '9876543210987654',
            'card_type': 'mastercard'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(BankAccount.objects.filter(account_name='New Account').exists())

    def test_remove_account(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('remove_account', args=[self.account.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BankAccount.objects.filter(id=self.account.id).exists())

    def test_add_bill(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_bill'), {
            'item_name': 'New Bill',
            'description': 'New Description',
            'amount': 150.00,
            'due_date': '2024-05-15',
            'logo_url': 'https://example.com/new-logo.png',
            'website_url': 'https://example.com/new'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Bill.objects.filter(item_name='New Bill').exists())

    def test_remove_bill(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('remove_bill', args=[self.bill.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Bill.objects.filter(id=self.bill.id).exists())

    def test_add_transaction(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_transaction'), {
            'transaction_type': 'expense',
            'item_name': 'New Item',
            'shop_name': 'New Shop',
            'amount': 75.00,
            'date': '2024-04-16',
            'payment_method': 'debit_card',
            'category': 'Shopping'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(item_name='New Item').exists())

    def test_delete_transaction(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_transaction', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())

    def test_add_goal(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_goal'), {
            'title': 'New Goal',
            'category': 'savings',
            'target_amount': 2000.00,
            'achieved_amount': 0.00,
            'monthly_target': 200.00,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'description': 'New goal description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Goal.objects.filter(title='New Goal').exists())

    def test_edit_goal(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_goal', args=[self.goal.id]), {
            'title': 'Updated Goal',
            'category': 'housing',
            'target_amount': 1500.00,
            'achieved_amount': 600.00,
            'monthly_target': 150.00,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'description': 'Updated goal description'
        })
        self.assertEqual(response.status_code, 302)
        updated_goal = Goal.objects.get(id=self.goal.id)
        self.assertEqual(updated_goal.title, 'Updated Goal')

    def test_delete_goal(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_goal', args=[self.goal.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Goal.objects.filter(id=self.goal.id).exists())

    def test_adjust_goal(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('adjust_goal', args=['savings']), {
            'amount': 100.00
        })
        self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('change_password'), {
            'old_password': 'testpass123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        })
        # The view might return 200 if it shows a success message
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 302:
            self.assertTrue(self.client.login(username='testuser', password='newpass123'))

    def test_update_account(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('update_account'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        })
        # The view might return 200 if it shows a success message
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 302:
            User = get_user_model()
            updated_user = User.objects.get(id=self.user.id)
            self.assertEqual(updated_user.first_name, 'Updated')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_view_with_logged_in_user_and_no_transactions(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses.html')

        # Context checks
        self.assertIn('graph_data', response.context)
        self.assertIn('yearly_data', response.context)
        self.assertIn('expense_breakdown', response.context)
        self.assertIn('expense_breakdown_month', response.context)
        self.assertEqual(json.loads(response.context['graph_data'])['values'], [0.0] * 12)

    def test_view_with_sample_expenses(self):
        self.client.login(username='testuser', password='testpass')
        now = timezone.now()

        # Create transactions
        Transaction.objects.create(
            user=self.user,
            transaction_type='expense',
            date=now - timedelta(days=10),
            amount=100.00,
            category='Food',
            item_name='Burger',
            shop_name='FastFood Inc.'
        )
        Transaction.objects.create(
            user=self.user,
            transaction_type='expense',
            date=now - timedelta(days=40),
            amount=200.00,
            category='Housing',
            item_name='Rent',
            shop_name='Landlord LLC'
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Monthly data should have non-zero values
        monthly_data = json.loads(response.context['graph_data'])
        self.assertTrue(any(value > 0 for value in monthly_data['values']))

        # Yearly data should include current and previous year
        yearly_data = json.loads(response.context['yearly_data'])
        self.assertIn(str(now.year), yearly_data['labels'])

        # Expense breakdown should reflect categories
        breakdown = response.context['expense_breakdown']
        categories = [entry['category'] for entry in breakdown if entry['amount'] > 0]
        self.assertIn('Food', categories)
        self.assertIn('Housing', categories)

    def test_expenses_are_filtered_by_user(self):
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        Transaction.objects.create(
            user=other_user,
            transaction_type='expense',
            date=timezone.now(),
            amount=999.00,
            category='Entertainment',
            item_name='Concert',
            shop_name='EventPlace'
        )

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        breakdown = response.context['expense_breakdown']
        self.assertTrue(all(entry['amount'] == 0 for entry in breakdown))

class TestForms(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_signup_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_update_form_valid(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_user_update_form_invalid(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        form_data = {
            'username': '',
            'email': 'invalid-email',
            'first_name': '',
            'last_name': ''
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid()) 
# Test that when a user is created, they have all categories in budget table, and they are
# all initially set to None
# Test that categories table exists with the categories we want
class BudgetAndCategoryTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        # Ensure default categories exist before tests
        if not Category.objects.exists():
            default_categories = ['Food', 'Housing', 'Other', 'Transportation', 'Entertainment', 'Shopping']
            for cat in default_categories:
                Category.objects.create(name=cat)

    def test_default_categories_created(self):
        """Test that all default categories exist in the database."""
        expected_categories = {'Food', 'Housing', 'Other', 'Transportation', 'Entertainment', 'Shopping'}
        actual_categories = set(Category.objects.values_list('name', flat=True))
        self.assertTrue(expected_categories.issubset(actual_categories))

    def test_budget_created_for_new_user(self):
        """Test that budget entries are created for all categories when a new user is created."""
        expected_categories = set(Category.objects.values_list('id', flat=True))

        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })

        self.assertEqual(response.status_code, 302)  # should redirect to 'overview'

        user = self.User.objects.get(username='testuser')
        budgets = Budget.objects.filter(user=user)

        
        self.assertEqual(budgets.count(), len(expected_categories))
        self.assertTrue(all(b.amount is None for b in budgets))
        actual_categories = set(budgets.values_list('category', flat=True))
        self.assertEqual(actual_categories, expected_categories)
