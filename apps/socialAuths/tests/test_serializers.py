# import pytest
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase
# from unittest.mock import MagicMock, patch
# from rest_framework.test import APITestCase
# from google.auth.transport import requests
# from google.oauth2 import id_token
# from .. import serializers 
# from rest_framework.exceptions import AuthenticationFailed
# import os
# from dotenv import load_dotenv
# load_dotenv()


# User = get_user_model()


# class GoogleTestCase(APITestCase):
#     @patch.object(requests, 'Request')
#     def test_validate_valid_token(self, mock_request):
#       mock_request.side_effect = MagicMock()
#       mock_idinfo = {
#           'iss': 'accounts.google.com',
#       }
#       mock_id_token = 'mock_id_token'

#       with patch.object(id_token, 'verify_oauth2_token', return_value=mock_idinfo) as mock_verify_token:
#           result = serializers.Google.validate(mock_id_token)
#           mock_verify_token.assert_called_once_with(mock_id_token, mock_request())
#           self.assertEqual(result, mock_idinfo)
            
    
#     @patch.object(requests, 'Request')
#     def test_validate_invalid_token(self, mock_request):
#         mock_request.side_effect = MagicMock()
#         mock_id_token = 'invalid_token'

#         with patch.object(id_token, 'verify_oauth2_token', side_effect=Exception):
#             result = serializers.Google.validate(mock_id_token)

#             self.assertEqual(result, "The token is either invalid or has expired")


# class GenerateUsernameTestCase(TestCase):
#     @patch.object(User.objects, 'filter')
#     def test_generate_username_does_not_exist(self, mock_filter):
#         name = "John Doe"
#         expected_username = "johndoe"
        
#         mock_filter.return_value.exists.return_value = False
#         result = serializers.generate_username(name)
#         self.assertEqual(result, expected_username)
#         mock_filter.assert_called_once_with(username=expected_username.lower())

#     @patch.object(User.objects, 'filter')
#     def test_generate_username_exists(self, mock_filter):
#         name = "John Doe"
#         existing_username = "johndoe"

#         mock_filter.return_value.exists.return_value = True
#         result = serializers.generate_username(name)
#         self.assertNotEqual(result, existing_username)
#         mock_filter.assert_called_once_with(username=existing_username.lower())

# class RegisterGoogleUserTestCase(APITestCase):
#     def setUp(self):
#         self.provider = 'google'
#         self.user_id = '123'
#         self.email = 'example@example.com'
#         self.name = 'John Doe'

#     @patch('apps.socialAuths.serializers.generate_username')
#     @patch.object(User.objects, 'filter')
#     def test_register_google_user_new_user(self, mock_filter, mock_generate_username):
#         mock_filter.return_value.exists.return_value = False
#         mock_generate_username.return_value = 'johndoe'

#         response = serializers.register_google_user(self.provider, self.user_id, self.email, self.name)
#         print("1 - ", response)

#         self.assertEqual(response['status'], 'signup successful')
#         self.assertEqual(response['name'], 'johndoe')
#         self.assertEqual(response['email'], self.email)
    
#     @patch.object(User.objects, 'filter')
#     def test_register_google_user_existing_user(self, mock_filter):
#         mock_filter.return_value.exists.return_value = True

#         with self.assertRaises(AuthenticationFailed):
#             serializers.register_google_user(self.provider, self.user_id, self.email, self.name)
            


# class LoginGoogleUserAPITestCase(APITestCase):
#     def setUp(self):
#       self.provider = 'google'
#       self.user_id = 'google_user_id'
#       self.email = 'test@example.com'
#       self.name = 'Test User'
#       self.password = 'secret'
#     #   self.secret = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET"),
      
#       self.user = User.objects.create_user(
#       email=self.email,
#       password=self.password
#       )
#       self.user.auth_provider = 'google'
#       self.user.save()
        
#     @patch.object(User.objects, 'filter')
#     @patch('apps.socialAuths.serializers.authenticate')
    ####stoppppp
    
    
    
    
    
    
    # def test_login_google_user_success(self, mock_filter, mock_authenticate):
    #     user = User.objects.create(email='test@example.com', password="password")
    #     mock_filter.return_value.exists.return_value = True
        
    #     response = serializers.register_google_user(self.provider, self.user_id, self.email, self.name)

       
    #     mock_authenticate.return_value = response.provider
        
      
    #     response = serializers.login_google_user(
    #         self.user['provider'], self.user['user_id'], self.user['email'], self.user['name']
    #     )

    #     self.assertEqual(response['status'], 'login successful')
    
    #dsfsdfsdf
    
    # def test_login_google_user_success(self, mock_filter, mock_authenticate):
    #     mock_filter.return_value = MagicMock(exists=MagicMock(return_value=True))
    #     mock_filter.return_value.first.return_value = self.user

    #     mock_authenticate.return_value = self.user
    #     os.environ['GOOGLE_OAUTH2_CLIENT_SECRET'] = self.password

    #     response = serializers.login_google_user(self.provider, self.user_id, self.email, self.name)
        
    #     self.assertEqual(response['status'], 'login successful')
    #     self.assertEqual(response['email'], self.user.email)
    #     self.assertIn('tokens', response)
        
    # def test_login_google_user_user_exists(self, mock_filter):
    #     # Create a mock user object
    #     mock_filter.return_value.exists.return_value = True
    #     print(mock_filter)
        

    #     # Call the login_google_user function
    #     result = login_google_user('google', 'user_id', 'test@example.com', 'Test User')

    #     # Check if the result indicates login successful
    #     self.assertEqual(result['status'], 'login successful')
  
    # def test_login_google_user_success(self, mock_filter, mock_authenticate):
    #       # Create a user with Google auth provider
    #       user = User.objects.create_user(email=self.email, password=self.client_secret)
    #       user.auth_provider = self.provider
    #       user.save()

    #       # Mock the User.objects.filter method to return the user
    #       mock_filter.return_value.exists.return_value = True
    #       print("1 - ", mock_filter.return_value.exists.return_value)
    #       mock_filter.return_value = [user]
    #       print("2 -", mock_filter.return_value)

    #       # Mock the authenticate method to return the user
    #       mock_authenticate.return_value = user
    #       print("3 -", mock_authenticate.return_value)

    #       # Set the GOOGLE_OAUTH2_CLIENT_SECRET environment variable
    #       with patch.dict('os.environ', {'GOOGLE_OAUTH2_CLIENT_SECRET': self.client_secret}):
    #           # Call the login_google_user function
    #           response = login_google_user(
    #               self.provider, self.user_id, self.email, self.name
    #           )

    #       # Verify the response
    #       self.assertEqual(response['status'], 'login successful')
    #       self.assertEqual(response['username'], user.username)
    #       self.assertEqual(response['email'], user.email)
    #       self.assertIn('access', response['tokens'])
    #       self.assertIn('refresh', response['tokens'])

    #       # Verify that the User.objects.filter method was called with the correct arguments
    #       mock_filter.assert_called_once_with(email=self.email)
    #       print(mock_filter)

    #       # Verify that the authenticate method was called with the correct arguments
    #       mock_authenticate.assert_called_once_with(
    #           email=self.email, password=self.client_secret)
          
    # def test_login_google_user_failure_user_not_found(self):
    #     # Mock the User.objects.filter method to return an empty queryset
    #     with patch.object(User.objects, 'filter') as mock_filter:
    #         mock_filter.return_value.exists.return_value = False

    #         # Call the login_google_user function and expect AuthenticationFailed exception
    #         with self.assertRaises(AuthenticationFailed):
    #             login_google_user(
    #                 self.provider, self.user_id, self.email, self.name
    #             )

    #             # Verify that the User.objects.filter method was called with the correct arguments
    #             mock_filter.assert_called_once_with(email=self.email)

    # def test_login_google_user_failure_different_auth_provider(self):
    #     # Create a user with a different auth provider
    #     user = User.objects.create_user(email=self.email, password=self.client_secret)
    #     user.auth_provider = 'facebook'
    #     user.save()

    #     # Mock the User.objects.filter method to return the user
    #     with patch.object(User.objects, 'filter') as mock_filter:
    #         mock_filter.return_value.exists.return_value = True
    #         mock_filter.return_value = [user]

    #         # Call the login_google_user function and expect AuthenticationFailed exception
    #         with self.assertRaises(AuthenticationFailed):
    #             login_google_user(
    #                 self.provider, self.user_id, self.email, self.name
    #             )

    #             # Verify that the User.objects.filter method was called with the correct arguments
    #             mock_filter.assert_called_once_with(email=self.email)
    