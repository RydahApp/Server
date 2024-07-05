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
        fields = ['product']


class CustomerProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProductReview
        fields = ['product', 'comment', 'rating', 'created_at', 'buyer']
        read_only_fields = ['created_at', 'buyer']

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['full_address', 'created_at', 'buyer', 'id']
        read_only_fields = ['id','created_at', 'buyer']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'content']