from django.db import models
from colorfield.fields import ColorField

CLOTHING_CHOICES = {
    "AB": "Abaya",
    "JI": "Jilbaab",
    "Niq": "Niqab",
    "Hi": "Hijaab",
    "DR": "Dress",
}

class ProductModel(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  price = models.PositiveIntegerField(default=0)
  color = ColorField(default='#FF0000')
  created_at = models.DateTimeField(auto_now=True)
  brand = models.CharField(max_length=100)
  size = models.CharField(max_length=250, default=None)
  catergory = models.CharField(max_length=20, choices=CLOTHING_CHOICES, default=None)
  images = models.FileField(upload_to = 'images/', default=None)
  in_stock = models.BooleanField(default=True)
  by_protect_fee = models.BooleanField(default=False)
  






