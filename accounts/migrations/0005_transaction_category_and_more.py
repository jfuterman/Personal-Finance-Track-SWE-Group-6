from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_transaction_category_icon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('Housing', 'Housing'), ('Food', 'Food'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment'), ('Shopping', 'Shopping'), ('Others', 'Others')], default='Others', max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer'), ('mobile_payment', 'Mobile Payment')], max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('expense', 'Expense'), ('revenue', 'Revenue')], max_length=10),
        ),
    ]
