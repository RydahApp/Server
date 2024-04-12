from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class CustomManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, password, date_of_birth, is_admin=False, is_active=True):
    now = timezone.now()
    user = self.model(
      first_name, 
      last_name, 
      username,
      email = self.normalize_email(email),
      date_of_birth=date_of_birth,
      last_login=now,
      date_joined=now,
    )
    user.is_admin=False
    user.is_active=True
    user.set_password(password)
    user.save(using=self._db)
  
  def create_superuser(self, email, password):
    user = self.create_user(
      email=email,
      password=password
    )
    user.is_admin=True
    user.is_active=True
    user.save(using=self._db)
  