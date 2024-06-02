from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.auths.models import User
import random
from rest_framework.exceptions import AuthenticationFailed
from google.auth.transport import requests
from google.oauth2 import id_token
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

class Google:
    """Google class to fetch the user info and return it"""
    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "The token is either invalid or has expired"


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_suffix = str(random.randint(0, 1000))
        new_username = username + str(random_suffix)
        return new_username
        # random_username = username + str(random.randint(0, 1000))
        # return generate_username(random_username)


def register_google_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():
        raise AuthenticationFailed(detail="User already registered... Proceed to login.")
    else:
        user = {
            'email': email,
            'password': os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
            }
        user = User.objects.create_user(**user)
        user.username = generate_username(name)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        return {
            'status': "signup successful",
            'name': user.username,
            'email': user.email,
        }


def login_google_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    print("not working")
    if filtered_user_by_email.exists():
        print("HRYYYY")
        print(filtered_user_by_email)
        print(filtered_user_by_email.exists())

        if provider == filtered_user_by_email[0].auth_provider:
            print("666", provider)
            print(filtered_user_by_email[0].auth_provider)
            registered_user = authenticate(
                email=email, password=os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET'))
            print("45", registered_user)
            return {
                'status': "login successful",
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
               

    else:
        raise AuthenticationFailed(detail="User Not Found... Kindly Proceed To Signup.")

class GoogleSignupSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')
        
        # if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
        #     raise AuthenticationFailed('Not Authorizied...')
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_google_user(
            provider=provider, user_id=user_id, email=email, name=name)
    
class GoogleLoginSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')
        
        # if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
        #     raise AuthenticationFailed('Not Authorizied...')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return login_google_user(
            provider=provider, user_id=user_id, email=email, name=name)



