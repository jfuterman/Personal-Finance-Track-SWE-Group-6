from django.contrib import admin
from django.urls import path
from accounts.views import (
    CustomLoginView, SignUpView, overview, balances, transactions,
    bills, expenses, goals, settings, add_account, add_bill, remove_bill,
    add_transaction, update_account, change_password, delete_transaction,
    add_goal, edit_goal, delete_goal, adjust_goal, home, remove_account
)
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', overview, name='overview'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', SignUpView.as_view(), name='register'),
    path('accounts/logout/', LogoutView.as_view(
        next_page=reverse_lazy('login'),
        template_name=None
    ), name='logout'),
    path('balances/', balances, name='balances'),
    path('transactions/', transactions, name='transactions'),
    path('bills/', bills, name='bills'),
    path('expenses/', expenses, name='expenses'),
    path('goals/', goals, name='goals'),
    path('settings/', settings, name='settings'),
    path('update-account/', update_account, name='update_account'),
    path('change-password/', change_password, name='change_password'),
    path('add-account/', add_account, name='add_account'),
    path('remove-account/<int:account_id>/', remove_account, name='remove_account'),
    path('add-bill/', add_bill, name='add_bill'),
    path('remove-bill/<int:bill_id>/', remove_bill, name='remove_bill'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('delete-transaction/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('add-goal/', add_goal, name='add_goal'),
    path('edit-goal/<int:goal_id>/', edit_goal, name='edit_goal'),
    path('delete-goal/<int:goal_id>/', delete_goal, name='delete_goal'),
    path('adjust-goal/<str:category>/', adjust_goal, name='adjust_goal'),
] 