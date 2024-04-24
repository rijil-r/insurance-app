from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from insurance.models import Customer, Policy


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create Customer
        password = 'password'
        customer = Customer.objects.create(username="john", first_name="John", last_name="Doe",
                                           email="john.doe@example.com", date_of_birth="1980-01-01",
                                           password=make_password(password))
        print(f"Customer created: {customer}")
        # Create Admin User
        user = get_user_model()
        admin = user.objects.create_superuser(username="admin", first_name="Admin", last_name="User",
                                              email="admin@example.com", password=make_password(password))
        print(f"Admin user created: {admin}")
        # Create multiple policies
        policy_types = ['Car Insurance', 'Home Insurance', 'Travel Insurance']
        for policy_type in policy_types:
            policy = Policy.objects.create(policy_type=policy_type, age_multiplier=0.02, premium_to_cover_ratio=0.02)
            print(f"Policy created: {policy}")
        print("Sample data created successfully")
