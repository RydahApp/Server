from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.response import Response
    
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

class ViewProductModelSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = ProductModel
        fields = '__all__'
        
    
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_instance = Category.objects.create(**category_data)
        product_instance = ProductModel.objects.create(category=category_instance, **validated_data)
        size_product_instance = ProductModel.objects.create(**validated_data)
        return product_instance, size_product_instance
    
  

class CreateProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
   

