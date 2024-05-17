from rest_framework import serializers
from .models import *
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        exclude = ['created_at', 'updated', 'seller', 'approve']
        read_only_fields = ['by_protect_fee', 'available_qty']

class ListProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        exclude = ['created_at', 'updated', 'seller', 'approve']
        read_only_fields = ['by_protect_fee', 'available_qty']

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavouriteProducts
        exclude = ['created_at', 'user']
