import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('credit', 'Credit Card'), ('checking', 'Checking'), ('savings', 'Savings'), ('investment', 'Investment'), ('loan', 'Loan')], max_length=20)),
                ('account_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=20)),
                ('bank_name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=1000.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
