from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomManager
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'apple': 'apple', 'google': 'google', 'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
  class Meta:
        app_label = 'auths'
        
  email = models.EmailField(unique=True, max_length=100)
  username = models.CharField(null=True, blank=True, max_length=100)
  first_name = models.CharField(null=True, blank=True, max_length=100)
  last_name = models.CharField(null=True, blank=True, max_length=100)
  last_login = models.DateTimeField(null=True, blank=True)
  date_joined = models.DateTimeField(auto_now_add=True)
  auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
  
  is_verified = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created =  models.DateTimeField(auto_now=True)

  otp = models.IntegerField(null=True,blank=True)
  activation_key = models.CharField(max_length=150,blank=True,null=True)
  user_secret_key = models.CharField(max_length=500,null=True,blank=True)
  
  REQUIRED_FIELDS = []
  USERNAME_FIELD = 'email'
  
  objects = CustomManager()
  
  @property
  def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"
  
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
  
class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=150)
  last_name = models.CharField(max_length=150)
  username = models.CharField(max_length=150)
  mobile_no = models.CharField(max_length=11)
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=700)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      verbose_name = ("UserProfile")
      verbose_name_plural = ("UserProfiles")

  def __str__(self):
      return self.email
  
  @property
  def full_name(self) -> str:
    return self.first_name + "" + self.last_name
