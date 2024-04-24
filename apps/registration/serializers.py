from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )
  class Meta:
    model = User
    fields = ['email', 'password']
    
  def validate_date_of_birth(self, date_of_birth):
      age = relativedelta(datetime.now(), date_of_birth).years

      if age < 18:
          raise serializers.ValidationError('Must be at least 18 years old to register.')
      else:
          return date_of_birth
      
  def create(self, validated_data):
    user = User.objects.create(
      # username = validated_data['username'],
      email = validated_data['email'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user
      
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {'bad_token': ('Token is expired or invalid')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=5, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['otp']