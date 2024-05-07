from rest_framework import serializers
from .models import ProductModel, Category, SizeVariant
from rest_framework import status
from rest_framework.response import Response
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = '__all__'


class ViewProductModelSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    size = SizeSerializer()
    
    class Meta:
        model = ProductModel
        fields = '__all__'
        
    
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_instance = Category.objects.create(**category_data)
        product_instance = ProductModel.objects.create(category=category_instance, **validated_data)
        size_data = validated_data.pop('size')
        size_instance = SizeVariant.objects.create(**size_data)
        size_product_instance = ProductModel.objects.create(size=size_instance, **validated_data)
        return product_instance, size_product_instance
    
  

class CreateProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
   

