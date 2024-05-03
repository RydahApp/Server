# from rest_framework import serializers
# from .models import ProductModel, ProductImageModel
# from rest_framework import status
# from rest_framework.response import Response

# class ImagesSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = ProductImageModel
#     fields = ('image', )
    
# class ProductSerializer(serializers.ModelSerializer):
#   color = serializers.StringRelatedField(many=True)
#   sizes = serializers.StringRelatedField(many=True)
#   images = serializers.SerializerMethodField()
  
#   def get_images(self, product):
#     return ImagesSerializer(product.product_images.all(), many=True).data
#   class Meta:
#     model = ProductModel
#     fields = ('id', 'name', 'description', 'price','in_stock','color','sizes','by_protect_fee','images')
  
#   def get_protect_fee(self, instance):
#       if instance.by_protect_fee:
#           price = instance.price
#           print(price)
#           if price < 500:
#               # Calculate protect fee for orders under £500
#               fixed_expense = 0.3
#               variable_percent = 3  # 3% variable cost
#               variable_cost = price * (variable_percent / 100)
#               protect_fee = fixed_expense + variable_cost
#           else:
#               # Calculate protect fee for orders of £500 or more
#               protect_fee = price * 0.03  # 3% of item's price
#           return protect_fee
#       else:
#           return 0

from rest_framework import serializers
from .models import ProductModel
from rest_framework.exceptions import PermissionDenied
from apps.auths.models import User

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user  # Set the user field to the authenticated user instance
        product = ProductModel.objects.create(**validated_data)
        return product
    

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise PermissionDenied("You do not have permission to update this product")
        return super().update(instance, validated_data)

    def delete(self, instance):
        user = self.context['request'].user
        if instance.user != user:
            raise PermissionDenied("You do not have permission to delete this product")
        instance.delete()