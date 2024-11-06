from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase



User = get_user_model()


class AdminAuthApiViewTest(APITestCase):  
    def test_admin_login(self):
        url = reverse('admin-login')
        
        # Test for invalid email
        data = {
            'email': 'notadmin@host.comm',
            'password': 'admin',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
         # Test for invalid password
        data = {
            'email': 'admin@host.com',
            'password': '!notadmin!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for not preveliged user
        data = {
            'email': 'user@host.com',
            'password': 'user',
        }
        User.objects.create(email=data['email'], password=data['password']).save()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
        
        # Test for invalid email
        data = {
            'email': 'user', 
            'password': 'user',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        
        # Test for valid credentials
        data = {
            'email': 'admin@host.com',
            'password': 'admin',
        }
        User.objects.create_superuser(email=data['email'], password=data['password'])
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        
        
    
        
        
        

