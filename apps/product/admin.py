from django.contrib import admin
from .models import ProductModel, Category, SizeVariant, ProductImage

    
admin.site.register(ProductModel)
admin.site.register(Category)
admin.site.register(SizeVariant)
admin.site.register(ProductImage)


