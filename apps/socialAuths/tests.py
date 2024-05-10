from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from unittest.mock import MagicMock, patch
from rest_framework.test import APITestCase
from google.auth.transport import requests
from google.oauth2 import id_token
from .serializers import Google
from .serializers import generate_username


User = get_user_model()


class GoogleTestCase(APITestCase):
    @patch.object(requests, 'Request')
    def test_validate_valid_token(self, mock_request):
      mock_request.side_effect = MagicMock()
      mock_idinfo = {
          'iss': 'accounts.google.com',
      }
      mock_id_token = 'mock_id_token'

      with patch.object(id_token, 'verify_oauth2_token', return_value=mock_idinfo) as mock_verify_token:
          result = Google.validate(mock_id_token)
          mock_verify_token.assert_called_once_with(mock_id_token, mock_request())
          self.assertEqual(result, mock_idinfo)
            
    
    @patch.object(requests, 'Request')
    def test_validate_invalid_token(self, mock_request):
        mock_request.side_effect = MagicMock()
        mock_id_token = 'invalid_token'

        with patch.object(id_token, 'verify_oauth2_token', side_effect=Exception):
            result = Google.validate(mock_id_token)

            self.assertEqual(result, "The token is either invalid or has expired")


class GenerateUsernameTestCase(TestCase):
    @patch.object(User.objects, 'filter')
    def test_generate_username_does_not_exist(self, mock_filter):
        name = "John Doe"
        expected_username = "johndoe"
        
        mock_filter.return_value.exists.return_value = False
        result = generate_username(name)
        self.assertEqual(result, expected_username)
        mock_filter.assert_called_once_with(username=expected_username.lower())

    @patch.object(User.objects, 'filter')
    def test_generate_username_exists(self, mock_filter):
        name = "John Doe"
        existing_username = "johndoe"

        mock_filter.return_value.exists.return_value = True
        result = generate_username(name)
        self.assertNotEqual(result, existing_username)
        mock_filter.assert_called_once_with(username=existing_username.lower())

      





