from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify
from apps.auths.models import User

class Category(models.Model):
  name = models.CharField(max_length=150)
  slug = models.SlugField(max_length=200, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)
  

class ProductModel(models.Model):
  seller = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=1500)
  price = models.PositiveIntegerField(default=0)
  color = ColorField(default='#FF0000')
  brand = models.CharField(max_length=100, null=True, blank=True)
  size = models.CharField(max_length=100)
  condition = models.CharField(max_length=100)
  available_qty = models.PositiveBigIntegerField(default=0)
  protection_fee = models.PositiveIntegerField(default=0, null=True, blank=True)
  by_protect_fee = models.BooleanField(default=False)
  approve = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class ProductImage(models.Model):
  seller = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to = 'images/product_images/') 
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.seller.email} - {self.product.name}'

class UserFavouriteProducts(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
      verbose_name = ("UserFavouriteProducts")
      verbose_name_plural = ("UserFavouriteProductss")

  def __str__(self):
      return f"{self.user.email} - {self.product.name}"

