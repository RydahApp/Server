from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone



class CustomManager(BaseUserManager):
  def create_user(self, email, password=None):
    if not email:
      raise ValueError("The Email must be set")
    if not password:
      raise ValueError("The Password must be set")


    user = self.model(email=self.normalize_email(email))
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password=None):
    if password is None:
        raise TypeError('Password should not be none')

    user = self.create_user(email, password)
    user.is_superuser = True
    user.is_admin = True
    user.save()
    return user