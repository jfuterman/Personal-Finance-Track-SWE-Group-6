import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_goal_monthly_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='card_type',
            field=models.CharField(choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='account_type',
            field=models.CharField(choices=[('credit', 'Credit Card'), ('checking', 'Checking'), ('savings', 'Savings'), ('investment', 'Investment'), ('loan', 'Loan')], max_length=50),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
