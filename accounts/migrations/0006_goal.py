import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_transaction_category_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('savings', 'Savings'), ('housing', 'Housing'), ('food', 'Food'), ('transportation', 'Transportation'), ('entertainment', 'Entertainment'), ('shopping', 'Shopping'), ('others', 'Others')], max_length=50)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('achieved_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['end_date'],
            },
        ),
    ]
