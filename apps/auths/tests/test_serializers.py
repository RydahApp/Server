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
from apps.auths.serializers import UserProfileSerializer
from apps.auths.models import User
from sendgrid.helpers.mail import Mail
from apps.auths.serializers import SetNewPasswordSerializer

@pytest.mark.django_db
class TestRegisterSerializer:
    @patch('apps.auths.serializers.RegisterEmailMessage')  # Mock the RegisterEmailMessage function
    @patch('apps.auths.serializers.generateKey')  # Mock the generateKey function
    def test_create_user_success(self, mock_generate_key, mock_register_email_message):
        # Mock the OTP and activation key
        mock_generate_key.return_value = {'OTP': '123456', 'totp': 'activation_key'}

        data = {
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()

        # Check user was created and saved correctly
        assert User.objects.count() == 1
        created_user = User.objects.get(email='newuser@example.com')
        assert created_user.email == 'newuser@example.com'
        assert check_password('password123', created_user.password)
        assert created_user.otp == 123456
        assert created_user.activation_key == 'activation_key'
        assert created_user.is_verified is False  # Assuming default is False for new users
        assert created_user.is_active is True  # Assuming default is True for new users

        # Check that email sending function was called
        mock_register_email_message.assert_called_once_with('newuser@example.com', '123456')
    
     
    @patch('apps.auths.serializers.RegisterEmailMessage')  # Mock the RegisterEmailMessage function
    @patch('apps.auths.serializers.generateKey')
    def test_create_user_with_existing_email(self, mock_generate_key, mock_register_email_message, user_factory):
        existing_user = user_factory()  # This will use the sequence to generate the email
        existing_email = existing_user.email
 
        # Attempt to create a new user with the same email
        data = {
            'email': existing_email,  # Use the email from the existing user
            'password': 'password123'
        }
        
        serializer = RegisterSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
            serializer.save()
    
    def test_create_user_password_not_provided(self):
        data = {
            'email': 'newuser@example.com',
            # Missing password
        }
        
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
   
     
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
        

@pytest.mark.django_db
class TestResetPasswordEmailRequestSerializer:
    
    @patch('apps.auths.serializers.ResetPasswordEmailMessage')
    @patch('apps.auths.serializers.generateKey')
    def test_valid_email(self, mock_generateKey, mock_ResetPasswordEmailMessage, user_factory):
        # Arrange
        user = user_factory()
        mock_generateKey.return_value = {'OTP': '123456', 'totp': 'some_activation_key'}
    
        data = {
            'email': user.email,
        }
    
        # Act
        serializer = ResetPasswordEmailRequestSerializer(data=data)
        is_valid = serializer.is_valid()
    
        # Assert
        assert is_valid is True
        validated_data = serializer.validated_data
    
        user.refresh_from_db()
        assert str(user.otp) == '123456'
        assert user.activation_key == 'some_activation_key'
        mock_ResetPasswordEmailMessage.assert_called_once_with(user.email, '123456')

    @patch('apps.auths.serializers.ResetPasswordEmailMessage')
    @patch('apps.auths.serializers.generateKey')
    def test_user_not_found(self, mock_generateKey, mock_ResetPasswordEmailMessage):
        # Arrange
        data = {
            'email': 'nonexistentuser@example.com',
        }

        # Act
        serializer = ResetPasswordEmailRequestSerializer(data=data)

        with pytest.raises(AuthenticationFailed, match="Invalid Email"):
            serializer.is_valid(raise_exception=True)
 
      
@pytest.mark.django_db
class TestSetNewPasswordSerializer:
    
    @patch('apps.auths.serializers.PasswordResetSuccessEmail')
    def test_valid_data(self, mock_PasswordResetSuccessEmail, user_factory):
        # Arrange
        user = user_factory()
        data = {
            'email': user.email,
            'password': 'new_password123',
        }
    
        # Act
        serializer = SetNewPasswordSerializer(data=data)
        is_valid = serializer.is_valid()
    
        # Assert
        assert is_valid is True
        validated_data = serializer.validated_data

        user.refresh_from_db()
        assert user.check_password('new_password123')
        mock_PasswordResetSuccessEmail.assert_called_once_with(user.email)

    def test_invalid_email(self):
        # Arrange
        data = {
            'email': 'nonexistent@example.com',
            'password': 'new_password123',
        }
    
        # Act
        serializer = SetNewPasswordSerializer(data=data)
    
        # Assert
        with pytest.raises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
class TestUserProfileSerializer:

    @pytest.fixture
    def existing_user(self):
        return User.objects.create(username='existing_user', email='user@example.com')

    @pytest.fixture
    def user_factory(self):
        # Factory method to create a user
        def _create_user(username, email):
            return User.objects.create(username=username, email=email)
        return _create_user

    @patch('apps.auths.serializers.User.objects.filter')
    def test_username_exists(self, mock_filter):
        # Arrange
        mock_filter.return_value.exists.return_value = True
        data = {
            'username': 'existing_user',
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newuser@example.com',
            'mobile_no': '07961972182',
            'location': '456 Another St, Othertown, USA',
        }

        # Act & Assert
        serializer = UserProfileSerializer(data=data)
        with pytest.raises(AuthenticationFailed, match='The username already exists'):
            serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
class TestPasswordHashing:
    def test_create_user_with_password_hashing(self):
        # Arrange
        data = {
            'email': 'testuser@example.com',
            'password': 'plain_password'
        }

        # Act
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            pytest.fail("Serializer validation failed")

        # Assert
        assert User.objects.count() == 1
        user = User.objects.first()
        assert check_password('plain_password', user.password), "Password was not hashed correctly"