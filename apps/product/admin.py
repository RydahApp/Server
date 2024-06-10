from django.contrib import admin
from .models import *

    
admin.site.register(ProductModel)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(UserFavouriteProducts)
admin.site.register(CustomerProductReview)


