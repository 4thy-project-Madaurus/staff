from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


# class PromoApiViewTest(APITestCase):
#     def test_create_promo(self):
#         url = reverse('promo-list')
        
#         data = {
#             'study_year': '1CP'
#         }
#         response = self.client.post(url, data=data, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
#     def test_retrieve_promo(self):
#         promo_data = {
#             'study_year': '1CP'
#         }
#         promo = Promo.objects.create(**promo_data)
#         promo_id = promo.pk
        
#         retrieve_response = self.client.get(reverse('promo-detail', kwargs={'pk': promo_id}))
        
#         self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
#         self.assertEqual(retrieve_response.data['study_year'], '1CP')

#     def test_delete_promo(self):
#         promo_data = {
#             'study_year': '1CP'
#         }
#         promo = Promo.objects.create(**promo_data)
#         promo_id = promo.pk
        
#         delete_response = self.client.delete(reverse('promo-detail', kwargs={'pk': promo_id}))
#         self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

# class GroupApiViewTest(APITestCase):
#     # def setUp(self):
#     #     self.promo = Promo.objects.create(study_year='1CP')

#     def test_create_group(self):
#         url = reverse('group-list')
#         group_data = {
#             'group': '1',
#             'promo': '1cp'
#         }
#         response = self.client.post(url, data=group_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_retrieve_group(self):
#         group = Group.objects.create(group='Group 2', promo="2cp")
#         url = reverse('group-detail', kwargs={'pk': group.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['group'], 'Group 2')
#         self.assertEqual(response.data['promo'], '2cp')

#     def test_update_group(self):
#         group = Group.objects.create(group='Group 3', promo='2cs')
#         url = reverse('group-detail', kwargs={'pk': group.pk})
#         updated_group_data = {
#             'group': 'Updated Group',
#             'promo':"2021"
#         }
#         response = self.client.put(url, data=updated_group_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Group.objects.get(pk=group.pk).group, 'Updated Group')

#     def test_delete_group(self):
#         group = Group.objects.create(group='Group 4', promo='3cs')
#         url = reverse('group-detail', kwargs={'pk': group.pk})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Group.objects.filter(pk=group.pk).exists())

