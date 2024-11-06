from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from teachers.models import Teacher

User = get_user_model()

class TeacherApiViewTest(APITestCase):

    def test_create_teacher(self):
        url = reverse('teacher-list')  
        data = {
            'user': {
                "email": "teacher@gmail.com",
                "password": "teacherpassword"
                },
            'position': 'Math Teacher',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a teacher object is created
        user = User.objects.get(email=data['user']['email'])
        self.assertTrue(Teacher.objects.filter(user=user).exists())

    def test_update_teacher(self):
        data = {
            'user': {
                "email": "teacher@gmail.com",
                "password": "teacherpassword"
            },
            'position': 'Math Teacher',
        }
        user = User.objects.create_user(email=data['user']['email'], password=data['user']['password'])
        teacher = Teacher.objects.create(user=user, position=data['position'])
        url = reverse('teacher-detail', kwargs={'pk': teacher.pk})  
        updated_data = {
            'position': 'Updated Math Teacher',
            'user': {
                'email': 'updated_teacher@gmail.com',
                'first_name': 'updated first name',
                'last_name': 'updated last name',
            }
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the teacher's data is updated in the database
        teacher.refresh_from_db()
   
        self.assertEqual(teacher.position, updated_data['position'])
        self.assertEqual(teacher.user.email, updated_data['user']['email'])
        self.assertEqual(teacher.user.first_name, updated_data['user']['first_name'])
        self.assertEqual(teacher.user.last_name, updated_data['user']['last_name'])

    def test_delete_teacher(self):
        data = {
            'user': {
                "email": "teacher@gmail.com",
                "password": "teacherpassword"
                },
            'position': 'Math Teacher',
        }
        user = User.objects.create_user(email=data['user']['email'], password=data['user']['password'])
        teacher = Teacher.objects.create(user=user, position=data['position'])
        url = reverse('teacher-detail', kwargs={'pk': teacher.pk}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

        # Check if the teacher is deleted from the database
        self.assertFalse(Teacher.objects.filter(pk=teacher.pk).exists())
