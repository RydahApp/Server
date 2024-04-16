from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )
  class Meta:
    model = User
    fields = ['email', 'password']
    
  def create(self, validated_data):
    user = User.objects.create(
      # username = validated_data['username'],
      email = validated_data['email'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user