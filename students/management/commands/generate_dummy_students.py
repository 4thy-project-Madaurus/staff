from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student
from faker import Faker
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate dummy data for Students'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create users and associated students
        for i in range(150):  # Adjust the range for the number of entries you want
            username = faker.user_name()
            avatar_url = f"https://avatars.githubusercontent.com/u/{i+500}"
            user = User.objects.create_user(
                avatar_url=avatar_url,
                username=username,
                password='password123',  # Use a constant password for simplicity
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                phone_number=faker.phone_number(),
                email=faker.email(),
                gender = faker.random_element(["Male", "Female"]), 
                city=faker.city()
            )

            group = f"{faker.random_letter().upper()}"
            student = Student.objects.create(
                user=user,
                group=group,
                promo=str(faker.random_int(min=2015, max=2024)),  
                year= faker.random_element(['1cp', '2cp', '1cs', '2cs', '3cs']),
                registration_number=f"REG{faker.random_number(digits=5)}"
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created student: {user.email}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated all dummy data'))
