from rest_framework import serializers
from .models import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .otp import *
from .utils import *
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
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
    user = User.objects.create(email = validated_data['email'])
    user.password = make_password(validated_data['password'])
    user.save()
    user_otp = generateKey()
 
    user = User.objects.get(email=validated_data['email'])
    user.otp = user_otp['OTP']

    user.activation_key = user_otp['totp']
    user.save()
    RegisterEmailMessage(user.email, user_otp['OTP'])
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
    full_name = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'full_name', 'tokens']

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

        fullname = ""
        if user.first_name and user.last_name:
            fullname = user.full_name
        
        return {
            'email': user.email,
            'username': user.username,
            'full_name': fullname,
            'tokens': user.tokens
        }
            
        return super().validate(attrs)
    
class EmailOTPVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['otp']
    
    def validate(self, attrs):
        
        otp = attrs.get('otp', '')
        
        # Your validation logic here
        
        return attrs

class EmailResendOTPVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        
        return attrs

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

                user_otp = generateKey()
                user.otp = user_otp['OTP']
                user.activation_key = user_otp['totp']
                user.save()
                ResetPasswordEmailMessage(user.email, user_otp['OTP'])
                return user
            else:
                raise ValidationError("User with email not found...", 401)
        except Exception as e:
            raise AuthenticationFailed('Invalid Email', 401)

class ResetPasswordEmailOTPVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['otp']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    email = serializers.EmailField(min_length=2)
    class Meta:
        model = User
        fields = ['password', 'email']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            email = attrs.get('email')
            if User.objects.filter(email=email).exists:
                user = User.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                PasswordResetSuccessEmail(email)
                return user
            else:
                raise ValidationError("Email Not Found!!!")
        except Exception as e:
            raise AuthenticationFailed('Something went wrong!!!', 401)
        return super().validate(attrs)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        username = attrs.get('username')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')

        if User.objects.filter(username=username).exists():
            raise AuthenticationFailed('The username already exists', 401)
        else:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return super().validate(attrs)
            else:
                raise ValidationError('Email Provided Does Not Match Signup Mail', 401)
        

