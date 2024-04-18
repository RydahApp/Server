from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from django.views.generic import View
# Create your views here.

class HomeView(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]
  
class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
  serializer_class = LoginSerializer
  permission_classes = [AllowAny]
  
  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
      
    if user is not None:
      login(request, user)
      print("YAYYY")
      return redirect('apps.registration:home')
    else:
      print("Error")
      return Response(messages.error(request, "Error"))

class LogOutView(generics.GenericAPIView):
  def get(self, request):
    username = request.data.get('username')
    logout(request)
    print(f"You are logged OUT {username}")
    return redirect('apps.registration:login')