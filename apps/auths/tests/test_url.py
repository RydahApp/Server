
# import pytest

# from django.urls import reverse
# ##Client
# @pytest.mark.django_db
# def test_view(client):
#    url = reverse('homepage-url')
#    response = client.get(url)
#    assert response.status_code == 200
   
   
# ##Admin Client 
# @pytest.mark.django_db
# def test_unauthorized(client):
# url = reverse('superuser-url')
# response = client.get(url)
# assert response.status_code == 401


# @pytest.mark.django_db
# def test_superuser_view(admin_client):
# url = reverse('superuser-url')
# response = admin_client.get(url)
# assert response.status_code == 200

# @pytest.mark.urls('myapp.test_urls')
# def test_something(client):
#     assert b'Success!' in client.get('/some_url_defined_in_test_urls/').content
    
# def test_with_authenticated_client(client, django_user_model):
# username = "user1"
# password = "bar"
# user = django_user_model.objects.create_user(username=username, password=password)
# # Use this:
# client.force_login(user)
# # Or this:
# client.login(username=username, password=password)
# response = client.get('/private')
# assert response.content == 'Protected Area'

# def test_an_admin_view(admin_client):
#     response = admin_client.get('/admin/')
#     assert response.status_code == 200













#   def test_user_can_register(self):
#     response = self.client.post(reverse('apps.auths:register'), self.user1)
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#   def test_user_can_register(self):
#     response = self.client.post(reverse('apps.auths:register'), self.user1)
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  
#   def test_empty_creditial(self):
#     response = self.client.post(reverse('apps.auths:register'), self.user2)
#     self.assertEqual(response.status_code, 400)
  
#   def admin_got_access_to_login(self):
#     response = self.client.post(reverse('apps.auths:login'), self.admin)
#     self.client.force_login(self.admin)
#     self.assertEqual(response.status_code, 200)
  
#   # def test_user_is_under_18(self):
#   #   response = self.client.post(reverse('apps.auths:register'), self.under_age_user)
#   #   self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#   #   self.assertEqual(response.data['date_of_birth'], ['Must be at least 18 years old to register.'])
  
#   def test_existing_user(self):
#     existing_user = User.objects.create_user(email='existing@example.com', password='test123')
#     self.same_as_existing_user = {'email': 'existing@example.com', 'password': 'test123', 'first_name': 'Existing', 'last_name': 'User'}    
#     response = self.client.post(reverse('apps.auths:register'), self.same_as_existing_user)
#     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     @patch('apps.auths.serializers.LoginSerializer.get_tokens', return_value={'refresh': 'refresh_token', 'access': 'access_token'})
#     def test_valid_login(self, mock_tokens):
#         login_data = {
#             'email': self.user_data['email'],
#             'password': self.user_data['password']
#         }
#         response = self.client.post(self.login_url, login_data)
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('tokens', response.data)
#         self.assertEqual(response.data['tokens']['refresh'], 'refresh_token')
#         self.assertEqual(response.data['tokens']['access'], 'access_token')
#         self.assertEqual(response.data['email'], self.user_data['email'])

#     # def test_wrong_creditials(self):
#     #   self.unregistered_user = {'email':'g@gmail.com', 'password':'g'}
#     #   response = self.client.post(reverse('apps.auths:login'), self.unregistered_user)
#     #   self.assertEqual(response.status_code, 403)
