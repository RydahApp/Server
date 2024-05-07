from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify

CLOTHING_CHOICES = {
    "Ab": "Abaya",
    "Ji": "Jilbaab",
    "Niq": "Niqab",
    "Hi": "Hijaab",
    "Dr": "Dress",
}

CLOTHING_SIZES = {
    "SM": "SMALL",
    "MED": "MEDIUM",
    "LRG": "LARGE",
}

class Category(models.Model):
  category_name = models.CharField(max_length=20, choices=CLOTHING_CHOICES, default=None)
  slug = models.SlugField(max_length=200, blank=True)
  
  def __str__(self):
    return self.category_name
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.category_name)
    super(Category, self).save(*args, **kwargs)

class SizeVariant(models.Model):
  size_name = models.CharField(max_length=100, choices=CLOTHING_SIZES, default=None)
  
  def __str__(self) -> str:
    return self.size_name
  

class ProductModel(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  product_name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  price = models.PositiveIntegerField(default=0)
  color = ColorField(default='#FF0000')
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  brand = models.CharField(max_length=100)
  images = models.ImageField(upload_to = 'images/')
  in_stock = models.BooleanField(default=True)
  by_protect_fee = models.BooleanField(default=False)
  
  size = models.ForeignKey(SizeVariant, blank=True, null=True, on_delete=models.PROTECT)

  def __str__(self):
    return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(ProductModel , on_delete=models.PROTECT)
    image = models.ImageField(upload_to = 'images/') 




