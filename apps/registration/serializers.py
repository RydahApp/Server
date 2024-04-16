from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, get_user_model


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
        style={'input_type': 'password'}
    )
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'username','email', 'password','date_of_birth']
    extra_kwargs = {'password': {'write_only': True}}
    
  def create(self, validated_data):
    user = User.objects.create(
      first_name = validated_data['first_name'],
      last_name = validated_data['last_name'],
      username = validated_data['username'],
      email = validated_data['email'],
      date_of_birth = validated_data['date_of_birth']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class LoginSerializer(serializers.Serializer):
  password = serializers.CharField(
        style={'input_type': 'password'}
    )
  class Meta:
    model = User
    fields = ['email', 'password']
    extra_kwargs = {'password': {'write_only': True}}
  
  def validate(self, data):
      username = data.get('email')
      password = data.get('password')

      if username and password:
          user = authenticate(request=self.context.get('request'),
                              username=username, password=password)
          if not user:
              msg = _('Unable to log in with provided credentials.')
              raise serializers.ValidationError(msg, code='authorization')
      else:
          msg = _('Must include "username" and "password".')
          raise serializers.ValidationError(msg, code='authorization')

      data['user'] = user
      return data