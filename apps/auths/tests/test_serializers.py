import pytest
from apps.auths.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.hashers import check_password

import pytest
from unittest.mock import patch
from django.contrib.auth.hashers import check_password
 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from apps.auths.serializers import EmailOTPVerificationSerializer
from rest_framework.exceptions import ValidationError
from apps.auths.serializers import EmailResendOTPVerificationSerializer
from apps.auths.serializers import ResetPasswordEmailRequestSerializer




@pytest.mark.django_db
@patch('apps.auths.serializers.RegisterEmailMessage')
@patch('apps.auths.serializers.generateKey')
def test_register_serializer_user_creation(mock_generateKey, mock_RegisterEmailMessage, user_factory):
    # Mock the generateKey function to return a specific OTP and activation key
    mock_generateKey.return_value = {'OTP': '123456', 'totp': 'some_activation_key'}

    email = 'test_unique@example.com'
    
    user_data = {
        'email': email,
        'password': 'testpassword123'
    }
    
    
    serializer = RegisterSerializer(data=user_data)
    assert serializer.is_valid(), serializer.errors
    
    user = serializer.save()
    
    # Check if the user is created with the correct email
    assert user.email == user_data['email']
    
    # Check if the password is hashed
    assert user.password != 'testpassword123'
    assert check_password('testpassword123', user.password)
    
    # Check if the OTP and activation key are set correctly
    assert user.otp == '123456'
    assert user.activation_key == 'some_activation_key'
    user.is_verified = True
    assert user.is_verified == True
    
    # Ensure the email sending function was called with the correct arguments
    mock_RegisterEmailMessage.assert_called_once_with(user.email, '123456')
    

class TestRegisterSerializer:
    @pytest.mark.django_db
    def test_age_validation(self):
        date_of_birth = (datetime.now() - relativedelta(years=17)).date()
        data = {
            'email': 'test@example.com',
            'password': 'strongpassword123',
            'date_of_birth': date_of_birth
        }
        class CustomRegisterSerializer(RegisterSerializer):
            date_of_birth = serializers.DateField()

            class Meta(RegisterSerializer.Meta):
                fields = RegisterSerializer.Meta.fields + ['date_of_birth']

        serializer = CustomRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'date_of_birth' in serializer.errors
        assert serializer.errors['date_of_birth'][0] == 'Must be at least 18 years old to register.'

@pytest.mark.django_db
class TestLoginSerializer:
    def test_valid_login(self, user_factory):
        user = user_factory()
        login_data = {
            'email': user.email,
            'password': 'defaultpassword' 
        }
        serializer = LoginSerializer(data=login_data)
        tokens = serializer.get_tokens(login_data)
        assert serializer.is_valid() == True
        assert 'refresh' in tokens
        assert 'access' in tokens
    
    def test_invalid_credentials(self):
        login_data = {
            'email': 'invalid',
            'password': 'invalidpassword'
        }
        serializer = LoginSerializer(data=login_data)
        assert serializer.is_valid() == False
        with pytest.raises(AuthenticationFailed):
            serializer.validate(login_data)
    
    def test_unverified_email(self, user_factory):
        user = user_factory(is_verified=False)
        login_data = {
            'email': user.email,
            'password': 'defaultpassword'
        }
        serializer = LoginSerializer(data=login_data)
        assert user.is_verified == False
        with pytest.raises(AuthenticationFailed):
            serializer.validate(login_data)
        
    def test_disabled_account(self, user_factory):
        user = user_factory(is_active=False)
        login_data = {
            'email': user.email,
            'password': 'defaultpassword'
        }

        serializer = LoginSerializer(data=login_data)
        assert user.is_active == False
        with pytest.raises(AuthenticationFailed):
          serializer.validate(login_data)
        
        
        
@pytest.mark.django_db
class TestEmailOTPVerificationSerializer:
    
    def test_valid_otp(self):
        # Valid OTP data
        valid_data = {'otp': 123456}
        
        # Create an instance of the serializer with valid data
        serializer = EmailOTPVerificationSerializer(data=valid_data)
        
        # Check if the serializer is valid
        assert serializer.is_valid() == True
        
        # Check if the OTP value is correctly validated
        assert serializer.validated_data['otp'] == 123456
    
    def test_invalid_otp(self):
        # Invalid OTP data (string instead of integer)
        invalid_data = {'otp': 'invalid_otp'}
        
        # Create an instance of the serializer with invalid data
        serializer = EmailOTPVerificationSerializer(data=invalid_data)
        
        # Check if the serializer is not valid
        assert serializer.is_valid() == False
        
        # Check if a ValidationError is raised with the correct error message
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        
        assert exc_info.value.detail == {'otp': ['A valid integer is required.']}

@pytest.mark.django_db
class TestEmailResendOTPVerificationSerializer:
    
    def test_valid_email(self, user_factory):
        # Create a user using the factory
        user = user_factory()
        
        # Valid email data
        valid_data = {'email': user.email}
        
        # Create an instance of the serializer with valid data
        serializer = EmailResendOTPVerificationSerializer(data=valid_data)
        
        # Check if the serializer is valid
        assert serializer.is_valid() == True
        
        # Check if the email value is correctly validated
        assert serializer.validated_data['email'] == user.email
    
    def test_invalid_email(self):
        # Invalid email data (missing '@' symbol)
        invalid_data = {'email': 'invalid_email'}
        
        # Create an instance of the serializer with invalid data
        serializer = EmailResendOTPVerificationSerializer(data=invalid_data)
        
        # Check if the serializer is not valid
        assert serializer.is_valid() == False
        
        # Check if a ValidationError is raised with the correct error message
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        
        assert exc_info.value.detail == {'email': ['Enter a valid email address.']}

# @pytest.mark.django_db
# class TestResetPasswordEmailRequestSerializer:
    
#     @patch('apps.auths.serializers.ResetPasswordEmailMessage')
#     @patch('apps.auths.serializers.generateKey')
#     def test_valid_email(self, mock_generateKey, mock_ResetPasswordEmailMessage, user_factory):
#         # Arrange
#         user = user_factory()
#         mock_generateKey.return_value = {'OTP': '123456', 'totp': 'some_activation_key'}
        
#         data = {
#             'email': user.email,
#         }

#         # Act
#         serializer = ResetPasswordEmailRequestSerializer(data=data)
#         is_valid = serializer.is_valid()
        
#         # Assert
#         assert is_valid == True
#         validated_data = serializer.validated_data
#         validated_user = serializer.validate(validated_data)
        
#         user.refresh_from_db()
#         assert user.otp == '123456'
#         assert user.activation_key == 'some_activation_key'
#         mock_ResetPasswordEmailMessage.assert_called_once_with(user.email, '123456')
        
