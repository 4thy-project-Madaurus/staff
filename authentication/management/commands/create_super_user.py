from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **kwargs):
        faker = Faker()
        email = 'admin@admin.com'

        if not User.objects.filter(email=email).exists():
            avatar_url = f"https://avatars.githubusercontent.com/u/1"
            user = User.objects.create_superuser(
                username='admin',
                email=email,
                password='password123',  
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                phone_number=faker.phone_number(),
                gender=faker.random_element(["Male", "Female"]),
                city=faker.city(),
                avatar_url=avatar_url
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {user.email}'))
        else:
            self.stdout.write(self.style.WARNING('Superuser with this email already exists'))

        self.stdout.write(self.style.SUCCESS('Command execution completed'))
