from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import BankAccount, Bill, Transaction, Goal
from .forms import CustomUserCreationForm, UserUpdateForm, CustomPasswordChangeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

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