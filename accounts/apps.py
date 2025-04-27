# This configuration file runs when Django reads the INSTALLED_APPS array on runserver or migrate.
# It is configured to add our desired categories to the database. 

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AccountsAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .models import Category
        # post_migrate runs after all migrations are applied.
        post_migrate.connect(create_default_categories, sender=self)

def create_default_categories(sender, **kwargs):
    from .models import Category 

    # list of default categories to create
    categories = ['Food', 'Housing', 'Other', 'Transportation', 'Entertainment', 'Shopping']
    
    # Create the categories if they don't exist
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)
