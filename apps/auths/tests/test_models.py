import pytest
from django.contrib.auth import authenticate
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.hashers import make_password

#TestingSuperUserModel
@pytest.mark.django_db
class TestCreateSuperUser:
  def test_create_superuser(self, admin_factory):
    admin = admin_factory()
    admin.email == 'admin1@gmail.com'
    assert admin.check_password('admin123')
    assert admin.is_superuser
      
#TestingUserModel
@pytest.mark.django_db
class TestCreateUser:
   def test_user_factory(self, user_factory):
      user = user_factory()
      assert user.first_name == 'Test1'
      assert user.last_name == 'Last1'
      assert user.email == 'test0@example.com'
      assert user.username == 'username0'
      assert user.is_verified == True
      assert user.is_active
      
# #TestCreateProfileModel
@pytest.mark.django_db
class TestCreateUserProfile:
   def test_user_profile_factory(self, user_profile_factory):
        user_profile = user_profile_factory()
        assert user_profile.first_name == 'Test1'
        assert user_profile.last_name == 'Last1'
        assert user_profile.email == user_profile.user.email
        assert user_profile.username.startswith('username')

# #TestUserCanCreateProfile

@pytest.mark.django_db
def test_user_can_create_profile(user_factory):
    user = user_factory()

    # Assert that the user object is created
    assert user is not None

    assert user.email.startswith('test')
    assert user.username.startswith('username')
    assert user.first_name == 'Test1'
    assert user.last_name == 'Last1'
    
    assert hasattr(user, 'userprofile')
    
    profile = user.userprofile
    assert profile.email == user.email
    assert profile.first_name == user.first_name
    assert profile.last_name == user.last_name
    assert profile.username == user.username


 
