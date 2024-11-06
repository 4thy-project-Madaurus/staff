from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from students.models import Student

User = get_user_model()

class StudentApiViewTest(APITestCase):
    # def setUp(self):
    #     self.group = Group.objects.create(group='Group 1', promo="1cp")

    def test_create_student(self):
        url = reverse('student-list')  
        data = {
            'user': {
                "email": "student@gmail.com",
                "password": "studentpassword"
            },
            'group': "1",
            'year': '2',
            'promo': '2021'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=data['user']['email'])
        self.assertTrue(Student.objects.filter(user=user).exists())

    def test_update_student(self):
        user = User.objects.create_user(email='student@gmail.com', password='studentpassword', first_name='Student', last_name='Last')
        student = Student.objects.create(user=user, group="1")

        url = reverse('student-detail', kwargs={'user_id': user.pk})  # Use 'pk' instead of 'user_id'

        updated_data = {
            'user': {  # Nested user data
                'email': 'updated_student@gmail.com',
                'first_name': 'Updated First Name',
                'last_name': 'Updated Last Name',
            },
            'group': "5",
            'year': '3',
            'promo': 'Promo3',  # Assuming promo is also updated
            'registration_number': 'REG12345',  # Assuming registration_number is also updated
        }

        response = self.client.put(url, updated_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        student.refresh_from_db()

        # Check updated user data
        self.assertEqual(student.user.email, updated_data['user']['email'])
        self.assertEqual(student.user.first_name, updated_data['user']['first_name'])
        self.assertEqual(student.user.last_name, updated_data['user']['last_name'])

        # Check updated student data
        self.assertEqual(student.group, f"{updated_data['year']}-{updated_data['group']}")
        self.assertEqual(student.promo, updated_data['promo'])
        self.assertEqual(student.registration_number, updated_data['registration_number'])
        
    def test_delete_student(self):
        user = User.objects.create_user(email='student@gmail.com', password='studentpassword')
        student = Student.objects.create(user=user, group="1")
        url = reverse('student-detail', kwargs={'user_id': user.pk}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Student.objects.filter(pk=student.pk).exists())



class CreateManyStudentsViewTest(APITestCase):
    def test_create_many_students(self):
        url = reverse('students-many')
        # group_1 = Group.objects.create(group='1', promo="1cs")
        # group_2 = Group.objects.create(group='2', promo="2cp")
        data = [
            {
                'user': {
                    'email': 'student1@example.com',
                    'password': 'password123',
                },
                'group': '1',
                'year':'2',
                'registration_number': '12345'
            },
            {
                'user': {
                    'email': 'student2@example.com',
                    'password': 'password456',
                },
                'group': '2',
                'year':'1',
                'registration_number': '67890'
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Student.objects.count(), 2)
        
        self.assertEqual(User.objects.filter(email='student1@example.com').count(), 1)
        self.assertEqual(User.objects.filter(email='student2@example.com').count(), 1)
        
        student1 = Student.objects.get(user__email='student1@example.com')
        student2 = Student.objects.get(user__email='student2@example.com')
        self.assertEqual(student1.group, f"{data[0]['year']}-{data[0]['group']}")
        self.assertEqual(student1.registration_number, data[0]['registration_number'])
        self.assertEqual(student2.group, f"{data[1]['year']}-{data[1]['group']}")
        self.assertEqual(student2.registration_number, data[1]['registration_number'])

    def test_create_many_students_invalid_data(self):
        url = reverse('students-many')

        data = [
            {
                'group': 'Group A',
                'registration_number': '12345'
            },
            {
                'user': {
                    'email': 'student2@example.com',
                    'password': 'password456',
                },
                'registration_number': '67890'
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
