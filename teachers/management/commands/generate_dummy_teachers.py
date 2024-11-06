from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from authentication.models import User  # Adjust if the User model is in another app
from teachers.models import Teacher  # Adjust if the Teacher model is in another app
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate dummy data for Teachers'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create users and associated teachers
        for i in range(150):  # Adjust the range for the number of entries you want
            avatar_url = f"https://avatars.githubusercontent.com/u/{i+200}"
            username = faker.user_name()
            user = User.objects.create_user(
                username=username,
                avatar_url=avatar_url,
                password='password123',  # Use a constant password for simplicity
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                phone_number=faker.phone_number(),
                gender = faker.random_element(["Male", "Female"]),
                city=faker.city()
            )

            # position = faker.job().replace('(', '').replace(')', '') 
            # classes = random.sample(['1CP', '2CP', '1CS', '2CS', '3CS'], k=faker.random_int(min=1, max=3))
            # courses = [faker.word() for _ in range(faker.random_int(min=1, max=5))]

            teacher = Teacher.objects.create(
                user=user,
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created teacher: {user.email}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated all dummy data'))
