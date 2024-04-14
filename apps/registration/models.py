from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .manager import CustomManager
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'apple': 'apple', 'google': 'google', 'email': 'email'}

class User(AbstractBaseUser):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(unique=True, max_length=100)
  username = models.CharField(max_length=50)
  date_of_birth = models.DateField(null=True)
  last_login = models.DateTimeField(null=True, blank=True)
  date_joined = models.DateTimeField(auto_now_add=True)
  auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
  
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created =  models.DateTimeField(auto_now=True)
  
  REQUIRED_FIELDS = ['username']
  USERNAME_FIELD = "email"
  
  objects = CustomManager()
  
  @property
  def full_name(self) -> str:
    return self.first_name + "" + self.last_name
  
  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True
    
  @property
  def is_staff(self):
      return self.is_admin

  def __str__(self):
      return self.email
  
  def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }