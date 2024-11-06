from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from teachers.models import Teacher
from students.models import Student

User = get_user_model()

class TeacherAuthApiViewTest(APITestCase):
    def test_teacher_login(self):
        url = reverse('login')
        
        # Test for invalid email
        data = {
            'email': 'notteacher@host.comm',
            'password': 'teacher',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for invalid password
        data = {
            'email': 'teacher@host.com',
            'password': '!notteacher!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for not privileged user
        data = {
            'email': 'user@host.com',
            'password': 'user',
        }
        user = User.objects.create(email=data['email'], password=data['password']).save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for invalid email format
        data = {
            'email': 'user', 
            'password': 'user',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for valid credentials
        data = {
            'email': 'teacher@host.com',
            'password': 'teacher',
        }
        user = User.objects.create_user(email=data['email'], password=data['password'])
        Teacher.objects.create(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        
    
    def test_student_login(self):
        url = reverse('login')
        
        # Test for invalid email
        data = {
            'email': 'notstudent@host.comm',
            'password': 'student',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for invalid password
        data = {
            'email': 'student@host.com',
            'password': '!notstudent!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for not privileged user
        data = {
            'email': 'user@host.com',
            'password': 'user',
        }
        user = User.objects.create(email=data['email'], password=data['password']).save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for invalid email format
        data = {
            'email': 'user', 
            'password': 'user',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for valid credentials
        data = {
            'email': 'student@host.com',
            'password': 'student',
        }
        user = User.objects.create_user(email=data['email'], password=data['password'])
        Student.objects.create(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

            