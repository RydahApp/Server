import pytest
from django.contrib.auth import authenticate
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
class TestCreateSuperUser:
  def test_create_superuser(self, admin_factory):
    admin = admin_factory()
    admin.email == 'admin1@gmail.com'
    assert admin.check_password('admin123')
    assert admin.is_superuser
    
@pytest.mark.django_db
class TestCreateUser:
   def test_user_factory(self, user_factory):
      user = user_factory()
      assert user.first_name == 'Test1'
      assert user.last_name == 'Last1'
      assert user.email == 'test0@example.com'
      assert user.username == 'username0'
      assert user.is_active

@pytest.mark.django_db
class TestCreateUserProfile:
   def test_user_profile_factory(self, user_profile_factory):
        user_profile = user_profile_factory()
        assert user_profile.first_name == 'Test1'
        assert user_profile.last_name == 'Last1'
        assert user_profile.email == user_profile.user.email
        assert user_profile.username.startswith('username')


@pytest.mark.django_db
def test_user_can_create_profile(user_factory):
    # Create a User using the factory
    user = user_factory()

    # Assert that the user object is created
    assert user is not None

    # Add assertions to test the attributes of the user
    assert user.email.startswith('test')
    assert user.username.startswith('username')
    assert user.first_name == 'Test1'
    assert user.last_name == 'Last1'
    # Add more assertions for other attributes if needed

    # Assert that the user has a profile
    
    assert hasattr(user, 'userprofile')
    
   # Add assertions to test the attributes of the profile
    profile = user.userprofile
    assert profile.email == user.email
    assert profile.first_name == user.first_name
    assert profile.last_name == user.last_name
    assert profile.username == user.username
    # Add more assertions for other attributes if needed

def test_profile_creation_without_being_user(user_profile_factory):
    # Attempt to create a UserProfile without a User
    with pytest.raises(Exception):
        user_profile = user_profile_factory()
        
#     def test_create_user_with_empty_email(self):
#         with pytest.raises(ValueError):
#             User.objects.create_user(email='', password='')


# @pytest.mark.django_db
# class TestPasswordHashing:
#     def test_password_is_hashed(self):
#         plain_password = 'testpassword123'
#         user = User.objects.create_user(
#             email='user@example.com',
#             password=plain_password
#         )
#         assert user.password != plain_password
#         assert user.password.startswith('pbkdf2_')
#         assert user.check_password(plain_password)
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
  
#   # def test_user_is_under_18(self):
#   #   response = self.client.post(reverse('apps.auths:register'), self.under_age_user)
#   #   self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#   #   self.assertEqual(response.data['date_of_birth'], ['Must be at least 18 years old to register.'])
  
#   def test_existing_user(self):
#     existing_user = User.objects.create_user(email='existing@example.com', password='test123')
#     self.same_as_existing_user = {'email': 'existing@example.com', 'password': 'test123', 'first_name': 'Existing', 'last_name': 'User'}    
#     response = self.client.post(reverse('apps.auths:register'), self.same_as_existing_user)
#     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# #admin can register 
 
# class LoginTestCase(APITestCase):
#     def setUp(self):
#         self.user_data = {
#             'email': 'testuser@example.com',
#             'password': 'strongpassword',
#         }
#         self.user = User.objects.create_user(**self.user_data)
#         self.user.is_verified = True
#         self.user.is_active = True
#         self.user.save()
#         self.login_url = reverse('apps.auths:login')  

    
#     @patch('apps.auths.serializers.LoginSerializer.get_tokens', return_value={'refresh': 'refresh_token', 'access': 'access_token'})
#     def test_valid_login(self, mock_tokens):
#         login_data = {
#             'email': self.user_data['email'],
#             'password': self.user_data['password']
#         }
#         response = self.client.post(self.login_url, login_data)
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('tokens', response.data)
#         self.assertEqual(response.data['tokens']['refresh'], 'refresh_token')
#         self.assertEqual(response.data['tokens']['access'], 'access_token')
#         self.assertEqual(response.data['email'], self.user_data['email'])

#     # def test_wrong_creditials(self):
#     #   self.unregistered_user = {'email':'g@gmail.com', 'password':'g'}
#     #   response = self.client.post(reverse('apps.auths:login'), self.unregistered_user)
#     #   self.assertEqual(response.status_code, 403)

# #admin can login
