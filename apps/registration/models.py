from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .manager import CustomManager

class User(AbstractBaseUser):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(unique=True, max_length=100)
  username = models.CharField(max_length=50)
  date_of_birth = models.DateField(null=True)
  last_login = models.DateTimeField(null=True, blank=True)
  date_joined = models.DateTimeField(auto_now_add=True)

  
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