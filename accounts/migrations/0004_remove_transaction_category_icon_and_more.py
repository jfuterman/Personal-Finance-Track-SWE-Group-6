from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category_icon',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='item_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('cash', 'Cash'), ('bank_transfer', 'Bank Transfer')], max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='shop_name',
            field=models.CharField(max_length=100),
        ),
    ]
