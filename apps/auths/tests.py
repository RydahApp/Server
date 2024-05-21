from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from auths.models import CustomUser as User

 
# User = get_user_model()


class UserModelTestCase(TestCase):
  def test_create_user(self):
    user = User.objects.create(
      first_name ='Test1',
      last_name='Last1',
      email='test@gmail.com',
      username='Test123',
      password='Test123',
      date_of_birth='1995-12-16'
    )
    self.assertEqual(user.first_name, 'Test1')
    self.assertEqual(user.last_name, 'Last1')
    self.assertEqual(user.email, 'test@gmail.com')
    self.assertEqual(user.date_of_birth,'1995-12-16')
    self.assertTrue(user.is_active)
    with self.assertRaises(ValueError):
      User.objects.create_user(username='', email='', password='')
  
  def test_create_superuser(self):
    admin = User.objects.create_superuser(
      username='admin',
      email='admin@gmail.com',
      password='admin123'
    )
    self.assertEqual(admin.username, 'admin')
    self.assertEqual(admin.email, 'admin@gmail.com')
    self.assertTrue(admin.is_staff)


# class RegisterTestCase(APITestCase):
#   def setUp(self):
#     self.user1 = { 
#     'first_name': 'test',
#     "last_name": 'code',
#     "username": 'test',
#     "email": 'test@gmail.com',
#     "date_of_birth": '1995-12-16',
#     "password": 'test123'
#     } 
#     self.user2 = { 
#     'first_name': '',
#     "last_name": '',
#     "username": '',
#     "email": '',
#     "date_of_birth": '1998-12-16',
#     "password": ''
#     } 
#     self.under_age_user = { 
#     'first_name': 'under_age',
#     "last_name": 'user',
#     "username": 'under_age',
#     "email": 'under_age@gmail.com',
#     "date_of_birth": '2024-01-16',
#     "password": 'under_age_user'
#     } 
#     self.admin = {'email': 'admin@example.com', 
#     'username':'admni', 
#     'password': 'admin123'
#     }
  
#   def test_user_can_register(self):
#     response = self.client.post(reverse('apps.auths:register'), self.user1)
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
#   def test_empty_creditial(self):
#     response = self.client.post(reverse('apps.auths:register'), self.user2)
#     self.assertEqual(response.status_code, 400)
  
#   def admin_got_access_to_login(self):
#     response = self.client.post(reverse('apps.auths:login'), self.admin)
#     self.client.force_login(self.admin)
#     self.assertEqual(response.status_code, 200)
  
#   def test_user_is_under_18(self):
#     response = self.client.post(reverse('apps.auths:register'), self.under_age_user)
#     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#     self.assertEqual(response.data['date_of_birth'], ['Must be at least 18 years old to register.'])
  
#   def test_existing_user(self):
#     existing_user = User.objects.create_user(email='existing@example.com', username='existing', password='test123')
#     self.same_as_existing_user = {'email': 'existing@example.com', 'username':'existing', 'password': 'test123', 'first_name': 'Existing', 'last_name': 'User'}    
#     response = self.client.post(reverse('apps.auths:register'), self.same_as_existing_user)
#     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# #admin can register 
    
# class LoginTestCase(APITestCase):
#     def setUp(self):
#       self.user = User.objects.create_user('test1gmail.com', "test", 'test123')

#     def test_user_can_login(self):
#       self.registered_user = {'username': 'test', 'email':'test1gmail.com', 'password':'test123'}
#       response = self.client.post(reverse('apps.auths:login'), self.registered_user)
#       self.assertEqual(response.status_code, 302)

#     def test_wrong_creditials(self):
#       self.unregistered_user = {'username': 'G', 'email':'g@gmail.com', 'password':'g'}
#       response = self.client.post(reverse('apps.auths:login'), self.unregistered_user)
#       self.assertEqual(response.status_code, 200)

# #admin can login
