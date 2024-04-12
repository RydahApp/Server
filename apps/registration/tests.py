from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth import authenticate
# Create your tests here.
 
User = get_user_model()

class UserModelTestCase(TestCase):
  def test_create_user(self):
    user = User.objects.create(
      first_name ="Test1",
      last_name="Last1",
      email="test@gmail.com",
      username="Test123",
      password="Test123"
    )
    self.assertEqual(user.first_name, "Test1")
    self.assertEqual(user.last_name, "Last1")
    self.assertEqual(user.email, "test@gmail.com")
    self.assertTrue(user.is_active)
    with self.assertRaises(ValueError):
      User.objects.create_user(first_name="", last_name="", email="", username="", password="")
  
  def test_create_superuser(self):
    admin_user = User.objects.create_superuser(
      username="Admin",
      email="adminuser@gmail.com",
      password="Admin123"
    )
    self.assertEqual(admin_user.username, "Admin")
    self.assertEqual(admin_user.email, "adminuser@gmail.com")
    self.assertTrue(admin_user.is_staff)
    
    self.assertTrue(authenticate(username="Admin", password="Admin123"))
    